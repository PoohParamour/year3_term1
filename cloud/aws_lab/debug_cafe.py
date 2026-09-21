import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
asg = boto3.client('autoscaling', region_name='us-east-1')
elbv2 = boto3.client('elbv2', region_name='us-east-1')

print("--- Launch Templates ---")
lts = ec2.describe_launch_templates()
for lt in lts['LaunchTemplates']:
    print(f"Name: {lt['LaunchTemplateName']}")
    vers = ec2.describe_launch_template_versions(LaunchTemplateId=lt['LaunchTemplateId'])
    for v in vers['LaunchTemplateVersions']:
        d = v['LaunchTemplateData']
        print(f"  ImageId: {d.get('ImageId')}, InstanceType: {d.get('InstanceType')}")
        print(f"  SecurityGroupIds: {d.get('SecurityGroupIds')}")
        print(f"  IamInstanceProfile: {d.get('IamInstanceProfile')}")
        print(f"  TagSpecifications: {d.get('TagSpecifications')}")

print("\n--- ASGs ---")
asgs = asg.describe_auto_scaling_groups()
for a in asgs['AutoScalingGroups']:
    print(f"ASG: {a['AutoScalingGroupName']}")
    print(f"  Instances: {len(a['Instances'])}")
    for inst in a['Instances']:
        print(f"    - {inst['InstanceId']} ({inst['LifecycleState']}, {inst['HealthStatus']})")
    print(f"  TargetGroups: {a['TargetGroupARNs']}")

print("\n--- Load Balancers ---")
lbs = elbv2.describe_load_balancers()
for lb in lbs['LoadBalancers']:
    print(f"LB: {lb['LoadBalancerName']} ({lb['State']['Code']})")

print("\n--- Target Groups ---")
tgs = elbv2.describe_target_groups()
for tg in tgs['TargetGroups']:
    print(f"TG: {tg['TargetGroupName']}")
    th = elbv2.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
    for h in th['TargetHealthDescriptions']:
        print(f"  - {h['Target']['Id']}: {h['TargetHealth']['State']} ({h['TargetHealth'].get('Reason', '')})")

