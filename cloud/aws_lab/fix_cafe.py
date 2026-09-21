import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
asg = boto3.client('autoscaling', region_name='us-east-1')
iam = boto3.client('iam', region_name='us-east-1')

print("1. Updating CafeSG...")
sgs = ec2.describe_security_groups()
cafe_sg = None
lb_sg = None
for sg in sgs['SecurityGroups']:
    if 'CafeSG' in sg['GroupName']: cafe_sg = sg['GroupId']
    if 'Cafe-LB-SG' in sg['GroupName']: lb_sg = sg['GroupId']

if cafe_sg and lb_sg:
    # Revoke 0.0.0.0/0
    try:
        ec2.revoke_security_group_ingress(
            GroupId=cafe_sg,
            IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]
        )
        print("Revoked 0.0.0.0/0 from CafeSG")
    except Exception as e:
        print(e)
    
    # Authorize from LB SG
    try:
        ec2.authorize_security_group_ingress(
            GroupId=cafe_sg,
            IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'UserIdGroupPairs': [{'GroupId': lb_sg}]}]
        )
        print("Authorized LB SG in CafeSG")
    except Exception as e:
        print(e)

print("2. Updating ASG Health Check Type...")
try:
    asg.update_auto_scaling_group(
        AutoScalingGroupName='Cafe-ASG',
        HealthCheckType='ELB',
        HealthCheckGracePeriod=90
    )
    print("Updated ASG to ELB health check")
except Exception as e:
    print(e)

print("3. Attaching SSM Policy to CafeRole...")
try:
    iam.attach_role_policy(
        RoleName='CafeRole',
        PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
    )
    print("Attached SSM Policy")
except Exception as e:
    print(e)
