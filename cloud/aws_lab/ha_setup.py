import boto3
import time
import base64

ec2 = boto3.client('ec2', region_name='us-east-1')
elbv2 = boto3.client('elbv2', region_name='us-east-1')
autoscaling = boto3.client('autoscaling', region_name='us-east-1')
rds = boto3.client('rds', region_name='us-east-1')

print("1. Identifying Resources...")
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['Lab VPC']}])
lab_vpc_id = vpcs['Vpcs'][0]['VpcId']
print(f"Lab VPC ID: {lab_vpc_id}")

subnets_info = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [lab_vpc_id]}])
public_subnet_1 = None
public_subnet_2 = None
private_subnet_1 = None
private_subnet_2 = None

for sn in subnets_info['Subnets']:
    name = ""
    for t in sn.get('Tags', []):
        if t['Key'] == 'Name':
            name = t['Value']
    if name == 'Public Subnet 1': public_subnet_1 = sn['SubnetId']
    if name == 'Public Subnet 2': public_subnet_2 = sn['SubnetId']
    if name == 'Private Subnet 1': private_subnet_1 = sn['SubnetId']
    if name == 'Private Subnet 2': private_subnet_2 = sn['SubnetId']

print(f"Public Subnets: {public_subnet_1}, {public_subnet_2}")
print(f"Private Subnets: {private_subnet_1}, {private_subnet_2}")

sgs = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [lab_vpc_id]}])
inventory_app_sg = None
inventory_db_sg = None
inventory_lb_sg = None
for sg in sgs['SecurityGroups']:
    if sg['GroupName'] == 'Inventory-App': inventory_app_sg = sg['GroupId']
    if sg['GroupName'] == 'Inventory-DB': inventory_db_sg = sg['GroupId']
    if sg['GroupName'] == 'Inventory-LB': inventory_lb_sg = sg['GroupId']

# Create Inventory-LB SG if it doesn't exist
if not inventory_lb_sg:
    print("Creating Inventory-LB Security Group...")
    sg_res = ec2.create_security_group(
        GroupName='Inventory-LB',
        Description='Enable web access to load balancer',
        VpcId=lab_vpc_id
    )
    inventory_lb_sg = sg_res['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=inventory_lb_sg,
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )

print("2. Creating Load Balancer and Target Group...")
lbs = elbv2.describe_load_balancers(Names=[])
lb_arn = None
for lb in lbs.get('LoadBalancers', []):
    if lb['LoadBalancerName'] == 'Inventory-LB':
        lb_arn = lb['LoadBalancerArn']

if not lb_arn:
    lb_res = elbv2.create_load_balancer(
        Name='Inventory-LB',
        Subnets=[public_subnet_1, public_subnet_2],
        SecurityGroups=[inventory_lb_sg],
        Scheme='internet-facing',
        Type='application'
    )
    lb_arn = lb_res['LoadBalancers'][0]['LoadBalancerArn']
print(f"Load Balancer ARN: {lb_arn}")

tgs = elbv2.describe_target_groups(Names=[])
tg_arn = None
for tg in tgs.get('TargetGroups', []):
    if tg['TargetGroupName'] == 'Inventory-App':
        tg_arn = tg['TargetGroupArn']

if not tg_arn:
    print("Creating Target Group...")
    tg_res = elbv2.create_target_group(
        Name='Inventory-App',
        Protocol='HTTP',
        Port=80,
        VpcId=lab_vpc_id,
        HealthCheckIntervalSeconds=10,
        HealthyThresholdCount=2,
        TargetType='instance'
    )
    tg_arn = tg_res['TargetGroups'][0]['TargetGroupArn']
print(f"Target Group ARN: {tg_arn}")

# Create Listener
listeners = elbv2.describe_listeners(LoadBalancerArn=lb_arn)
if not listeners['Listeners']:
    print("Creating ALB Listener...")
    elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[{'Type': 'forward', 'TargetGroupArn': tg_arn}]
    )

print("3. Creating AMI from Web Server 1...")
instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['Web Server 1']}])
web_server_1_id = None
for r in instances['Reservations']:
    for i in r['Instances']:
        if i['State']['Name'] in ['running', 'stopped']:
            web_server_1_id = i['InstanceId']

ami_id = None
images = ec2.describe_images(Filters=[{'Name': 'name', 'Values': ['Web Server AMI']}])
if images['Images']:
    ami_id = images['Images'][0]['ImageId']
    print(f"AMI already exists: {ami_id}")
else:
    print(f"Creating AMI from {web_server_1_id}...")
    ami_res = ec2.create_image(
        InstanceId=web_server_1_id,
        Name='Web Server AMI',
        Description='Lab AMI for Web Server',
        NoReboot=True
    )
    ami_id = ami_res['ImageId']
    print(f"Waiting for AMI {ami_id} to be available...")
    waiter = ec2.get_waiter('image_available')
    waiter.wait(ImageIds=[ami_id])

print("4. Creating Launch Template and Auto Scaling Group...")
lt_name = 'Inventory-LT'
lts = ec2.describe_launch_templates(Filters=[{'Name': 'launch-template-name', 'Values': [lt_name]}])
if not lts['LaunchTemplates']:
    print("Creating Launch Template...")
    user_data = '''#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd mysql
amazon-linux-extras install -y php7.2
# Download Lab files
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACACAD-3-113230/12-lab-mod10-guided-Scaling/s3/scripts/inventory-app.zip
unzip inventory-app.zip -d /var/www/html/
# Download and install the AWS SDK for PHP
wget https://github.com/aws/aws-sdk-php/releases/download/3.62.3/aws.zip
unzip aws -d /var/www/html
# Turn on web server
chkconfig httpd on
service httpd start'''
    user_data_b64 = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')
    
    ec2.create_launch_template(
        LaunchTemplateName=lt_name,
        LaunchTemplateData={
            'ImageId': ami_id,
            'InstanceType': 't2.micro',
            'KeyName': 'vockey',
            'SecurityGroupIds': [inventory_app_sg],
            'IamInstanceProfile': {'Name': 'Inventory-App-Role'},
            'Monitoring': {'Enabled': True},
            'UserData': user_data_b64
        }
    )

asg_name = 'Inventory-ASG'
asgs = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
if not asgs['AutoScalingGroups']:
    print("Creating Auto Scaling Group...")
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={'LaunchTemplateName': lt_name},
        MinSize=2,
        MaxSize=2,
        DesiredCapacity=2,
        VPCZoneIdentifier=f"{private_subnet_1},{private_subnet_2}",
        TargetGroupARNs=[tg_arn],
        HealthCheckType='ELB',
        HealthCheckGracePeriod=90,
        Tags=[{'Key': 'Name', 'Value': 'Inventory-App', 'PropagateAtLaunch': True}]
    )
    autoscaling.enable_metrics_collection(
        AutoScalingGroupName=asg_name,
        Granularity='1Minute'
    )

print("5. Updating Security Groups...")
# Inventory-App: Allow HTTP from Inventory-LB
try:
    ec2.authorize_security_group_ingress(
        GroupId=inventory_app_sg,
        IpPermissions=[{
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'UserIdGroupPairs': [{'GroupId': inventory_lb_sg, 'Description': 'Traffic from load balancer'}]
        }]
    )
    print("Updated Inventory-App SG.")
except Exception as e:
    if 'InvalidPermission.Duplicate' not in str(e): print(e)

# Inventory-DB: Delete existing rules and allow MYSQL from Inventory-App
db_sg_info = ec2.describe_security_groups(GroupIds=[inventory_db_sg])['SecurityGroups'][0]
if db_sg_info['IpPermissions']:
    ec2.revoke_security_group_ingress(
        GroupId=inventory_db_sg,
        IpPermissions=db_sg_info['IpPermissions']
    )
try:
    ec2.authorize_security_group_ingress(
        GroupId=inventory_db_sg,
        IpPermissions=[{
            'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306,
            'UserIdGroupPairs': [{'GroupId': inventory_app_sg, 'Description': 'Traffic from application servers'}]
        }]
    )
    print("Updated Inventory-DB SG.")
except Exception as e:
    if 'InvalidPermission.Duplicate' not in str(e): print(e)

print("6. Modifying RDS to Multi-AZ (Optional Task 1)...")
try:
    rds.modify_db_instance(
        DBInstanceIdentifier='inventory-db',
        MultiAZ=True,
        DBInstanceClass='db.t3.small',
        AllocatedStorage=20,
        ApplyImmediately=True
    )
    print("RDS modification started.")
except Exception as e:
    print(f"RDS modify info: {e}")

print("7. Creating NAT Gateway 2 and Route Table (Optional Task 2)...")
nat_gws = ec2.describe_nat_gateways(Filters=[{'Name': 'subnet-id', 'Values': [public_subnet_2]}])
nat_gw_id = None
if nat_gws['NatGateways'] and nat_gws['NatGateways'][0]['State'] != 'deleted':
    nat_gw_id = nat_gws['NatGateways'][0]['NatGatewayId']
    print(f"NAT Gateway already exists: {nat_gw_id}")
else:
    print("Allocating Elastic IP for NAT Gateway 2...")
    eip_res = ec2.allocate_address(Domain='vpc')
    print("Creating NAT Gateway 2...")
    nat_res = ec2.create_nat_gateway(SubnetId=public_subnet_2, AllocationId=eip_res['AllocationId'])
    nat_gw_id = nat_res['NatGateway']['NatGatewayId']
    ec2.create_tags(Resources=[nat_gw_id], Tags=[{'Key': 'Name', 'Value': 'NatGateway2'}])

# Route Table for Private Subnet 2
rt_name = 'Private Route Table 2'
rts = ec2.describe_route_tables(Filters=[{'Name': 'tag:Name', 'Values': [rt_name]}])
rt_id = None
if rts['RouteTables']:
    rt_id = rts['RouteTables'][0]['RouteTableId']
else:
    print("Creating Private Route Table 2...")
    rt_res = ec2.create_route_table(VpcId=lab_vpc_id)
    rt_id = rt_res['RouteTable']['RouteTableId']
    ec2.create_tags(Resources=[rt_id], Tags=[{'Key': 'Name', 'Value': rt_name}])
    
    # Wait for NAT GW to be available before adding route
    print("Waiting for NAT Gateway to be available...")
    waiter = ec2.get_waiter('nat_gateway_available')
    waiter.wait(NatGatewayIds=[nat_gw_id])
    
    print("Adding route to NAT Gateway 2...")
    ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', NatGatewayId=nat_gw_id)
    
    print("Associating Route Table with Private Subnet 2...")
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=private_subnet_2)

print("\nSetup Finished Successfully!")
