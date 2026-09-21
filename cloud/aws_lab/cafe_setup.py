import boto3
import time
import os

ec2 = boto3.client('ec2', region_name='us-east-1')
elbv2 = boto3.client('elbv2', region_name='us-east-1')
autoscaling = boto3.client('autoscaling', region_name='us-east-1')

print("1. Identifying Resources...")
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['Lab VPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']
print(f"VPC ID: {vpc_id}")

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
public_subnet_1 = None
public_subnet_2 = None
private_subnet_1 = None
private_subnet_2 = None

for sn in subnets['Subnets']:
    name = next((t['Value'] for t in sn.get('Tags', []) if t['Key'] == 'Name'), "")
    if name == 'Public Subnet 1': public_subnet_1 = sn['SubnetId']
    if name == 'Public Subnet 2': public_subnet_2 = sn['SubnetId']
    if name == 'Private Subnet 1': private_subnet_1 = sn['SubnetId']
    if name == 'Private Subnet 2': private_subnet_2 = sn['SubnetId']

print(f"Public Subnets: {public_subnet_1}, {public_subnet_2}")
print(f"Private Subnets: {private_subnet_1}, {private_subnet_2}")

sgs = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
cafe_sg = None
for sg in sgs['SecurityGroups']:
    if 'CafeSG' in sg['GroupName']: cafe_sg = sg['GroupId']

images = ec2.describe_images(Owners=['self'])
ami_id = None
for image in images['Images']:
    if image['Name'] == 'Cafe WebServer Image': ami_id = image['ImageId']
print(f"AMI ID: {ami_id}")

rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
private_rt_2 = None
for rt in rts['RouteTables']:
    name = next((t['Value'] for t in rt.get('Tags', []) if t['Key'] == 'Name'), "")
    if name == 'Private Route Table 2': private_rt_2 = rt['RouteTableId']

print("2. Creating NAT Gateway and Updating Route Table...")
nat_gws = ec2.describe_nat_gateways(Filters=[{'Name': 'subnet-id', 'Values': [public_subnet_2]}])
nat_gw_id = None
if nat_gws['NatGateways'] and nat_gws['NatGateways'][0]['State'] != 'deleted':
    nat_gw_id = nat_gws['NatGateways'][0]['NatGatewayId']
    print(f"NAT Gateway already exists: {nat_gw_id}")
else:
    print("Allocating Elastic IP for NAT Gateway 2...")
    eip_res = ec2.allocate_address(Domain='vpc')
    print("Creating NAT Gateway in Public Subnet 2...")
    nat_res = ec2.create_nat_gateway(SubnetId=public_subnet_2, AllocationId=eip_res['AllocationId'])
    nat_gw_id = nat_res['NatGateway']['NatGatewayId']
    
    print("Waiting for NAT Gateway to be available...")
    waiter = ec2.get_waiter('nat_gateway_available')
    waiter.wait(NatGatewayIds=[nat_gw_id])
    
print("Adding route to NAT Gateway 2 in Private Route Table 2...")
try:
    ec2.create_route(RouteTableId=private_rt_2, DestinationCidrBlock='0.0.0.0/0', NatGatewayId=nat_gw_id)
except Exception as e:
    if 'RouteAlreadyExists' not in str(e): print(e)

print("3. Creating Key Pair and Launch Template...")
try:
    key_res = ec2.create_key_pair(KeyName='CafeKey')
    with open('CafeKey.pem', 'w') as f:
        f.write(key_res['KeyMaterial'])
    os.chmod('CafeKey.pem', 0o400)
    print("Created Key Pair 'CafeKey'")
except Exception as e:
    if 'InvalidKeyPair.Duplicate' not in str(e): print(e)

lt_name = 'Cafe-LT'
lts = ec2.describe_launch_templates(Filters=[{'Name': 'launch-template-name', 'Values': [lt_name]}])
if not lts['LaunchTemplates']:
    ec2.create_launch_template(
        LaunchTemplateName=lt_name,
        LaunchTemplateData={
            'ImageId': ami_id,
            'InstanceType': 't2.micro',
            'KeyName': 'CafeKey',
            'SecurityGroupIds': [cafe_sg],
            'IamInstanceProfile': {'Name': 'CafeRole'},
            'TagSpecifications': [
                {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'webserver'}]}
            ]
        }
    )
    print("Created Launch Template 'Cafe-LT'")

print("4. Creating Load Balancer and Target Group...")
# Create SG for LB
lb_sg_name = 'Cafe-LB-SG'
lb_sg_id = None
for sg in sgs['SecurityGroups']:
    if sg['GroupName'] == lb_sg_name: lb_sg_id = sg['GroupId']

if not lb_sg_id:
    sg_res = ec2.create_security_group(GroupName=lb_sg_name, Description='Allow HTTP', VpcId=vpc_id)
    lb_sg_id = sg_res['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=lb_sg_id,
        IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]
    )
    print(f"Created SG {lb_sg_name}")

lbs = elbv2.describe_load_balancers(Names=[])
lb_arn = None
for lb in lbs.get('LoadBalancers', []):
    if lb['LoadBalancerName'] == 'Cafe-LB': lb_arn = lb['LoadBalancerArn']

if not lb_arn:
    lb_res = elbv2.create_load_balancer(
        Name='Cafe-LB',
        Subnets=[public_subnet_1, public_subnet_2],
        SecurityGroups=[lb_sg_id],
        Scheme='internet-facing',
        Type='application'
    )
    lb_arn = lb_res['LoadBalancers'][0]['LoadBalancerArn']
    print(f"Created Load Balancer 'Cafe-LB': {lb_arn}")

tgs = elbv2.describe_target_groups(Names=[])
tg_arn = None
for tg in tgs.get('TargetGroups', []):
    if tg['TargetGroupName'] == 'Cafe-TG': tg_arn = tg['TargetGroupArn']

if not tg_arn:
    tg_res = elbv2.create_target_group(
        Name='Cafe-TG',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        TargetType='instance'
    )
    tg_arn = tg_res['TargetGroups'][0]['TargetGroupArn']
    print(f"Created Target Group 'Cafe-TG': {tg_arn}")

listeners = elbv2.describe_listeners(LoadBalancerArn=lb_arn)
if not listeners['Listeners']:
    elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[{'Type': 'forward', 'TargetGroupArn': tg_arn}]
    )
    print("Created Listener for Load Balancer")

print("5. Creating Auto Scaling Group and Scaling Policy...")
asg_name = 'Cafe-ASG'
asgs = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
if not asgs['AutoScalingGroups']:
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={'LaunchTemplateName': lt_name},
        MinSize=2,
        MaxSize=6,
        DesiredCapacity=2,
        VPCZoneIdentifier=f"{private_subnet_1},{private_subnet_2}",
        TargetGroupARNs=[tg_arn]
    )
    print("Created Auto Scaling Group 'Cafe-ASG'")
    
    # Target Tracking Scaling Policy
    autoscaling.put_scaling_policy(
        AutoScalingGroupName=asg_name,
        PolicyName='Cafe-Target-Tracking',
        PolicyType='TargetTrackingScaling',
        TargetTrackingConfiguration={
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ASGAverageCPUUtilization'
            },
            'TargetValue': 25.0,
            'DisableScaleIn': False
        },
        EstimatedInstanceWarmup=60
    )
    print("Added Target Tracking Scaling Policy")

print("\nCafe Challenge Lab Setup Finished Successfully!")
