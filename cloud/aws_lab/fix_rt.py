import boto3
ec2 = boto3.client('ec2', region_name='us-east-1')

# Get VPC ID
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['Lab VPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

# Get Private Subnet 2 ID
subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
private_subnet_2 = None
for sn in subnets['Subnets']:
    for t in sn.get('Tags', []):
        if t['Key'] == 'Name' and t['Value'] == 'Private Subnet 2':
            private_subnet_2 = sn['SubnetId']

# Get Route Table ID
rts = ec2.describe_route_tables(Filters=[{'Name': 'tag:Name', 'Values': ['Private Route Table 2']}])
rt_id = rts['RouteTables'][0]['RouteTableId']

print(f"Subnet: {private_subnet_2}, Route Table: {rt_id}")

# Find existing association
all_rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
assoc_id = None
for r in all_rts['RouteTables']:
    for a in r.get('Associations', []):
        if a.get('SubnetId') == private_subnet_2:
            assoc_id = a['RouteTableAssociationId']
            break

if assoc_id:
    print(f"Replacing association {assoc_id}...")
    ec2.replace_route_table_association(AssociationId=assoc_id, RouteTableId=rt_id)
else:
    print("Associating...")
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=private_subnet_2)

print("Fixed successfully!")
