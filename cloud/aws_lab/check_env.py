import boto3
ec2 = boto3.client('ec2', region_name='us-east-1')

print("--- Security Groups ---")
sgs = ec2.describe_security_groups()
for sg in sgs['SecurityGroups']:
    if 'CafeSG' in sg['GroupName']:
        print(f"CafeSG Inbound Rules:")
        for perm in sg['IpPermissions']:
            print(f"  Port: {perm.get('FromPort')} to {perm.get('ToPort')}, IP Ranges: {perm.get('IpRanges')}")

print("\n--- Subnets & Route Tables ---")
subnets = ec2.describe_subnets()
for sn in subnets['Subnets']:
    name = next((t['Value'] for t in sn.get('Tags', []) if t['Key'] == 'Name'), sn['SubnetId'])
    print(f"Subnet: {name} (Auto-assign public IP: {sn['MapPublicIpOnLaunch']})")
    
rts = ec2.describe_route_tables()
for rt in rts['RouteTables']:
    name = next((t['Value'] for t in rt.get('Tags', []) if t['Key'] == 'Name'), rt['RouteTableId'])
    print(f"Route Table: {name}")
    for route in rt['Routes']:
        print(f"  Route: {route.get('DestinationCidrBlock')} -> {route.get('GatewayId', route.get('NatGatewayId'))}")

print("\n--- Instances ---")
instances = ec2.describe_instances()
for r in instances['Reservations']:
    for i in r['Instances']:
        name = next((t['Value'] for t in i.get('Tags', []) if t['Key'] == 'Name'), i['InstanceId'])
        print(f"Instance: {name}, Public IP: {i.get('PublicIpAddress')}")

print("\n--- AMIs ---")
images = ec2.describe_images(Owners=['self'])
for image in images['Images']:
    print(f"AMI Name: {image.get('Name')}")
