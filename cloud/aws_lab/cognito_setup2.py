import boto3

cognito = boto3.client('cognito-idp', region_name='us-east-1')
cognito_id = boto3.client('cognito-identity', region_name='us-east-1')

user_pool_id = 'us-east-1_EnXFJiywq'
client_id = '5f3e94ero802m5mcf42ms801eq'
domain_prefix = 'bird-app-domain-yh9q2i6f'

print("Creating user 'admin'...")
try:
    cognito.admin_create_user(
        UserPoolId=user_pool_id,
        Username='admin',
        UserAttributes=[
            {'Name': 'email', 'Value': 'admin@example.com'},
            {'Name': 'email_verified', 'Value': 'true'}
        ],
        MessageAction='SUPPRESS',
        TemporaryPassword='Admin123$'
    )
except Exception as e:
    print(f"User admin may already exist or error: {e}")

print("Creating group 'Administrators'...")
try:
    cognito.create_group(
        GroupName='Administrators',
        UserPoolId=user_pool_id
    )
except Exception as e:
    print(f"Group may already exist or error: {e}")

print("Adding 'admin' to 'Administrators'...")
try:
    cognito.admin_add_user_to_group(
        UserPoolId=user_pool_id,
        Username='admin',
        GroupName='Administrators'
    )
except Exception as e:
    print(f"Error adding to group: {e}")

print("Finding Identity Pool 'bird_app_id_pool'...")
id_pools = cognito_id.list_identity_pools(MaxResults=50)
identity_pool_id = None
for pool in id_pools['IdentityPools']:
    if pool['IdentityPoolName'] == 'bird_app_id_pool':
        identity_pool_id = pool['IdentityPoolId']
        break

if not identity_pool_id:
    print("WARNING: Identity pool not found! Searching for similarly named pool...")
    if id_pools['IdentityPools']:
        identity_pool_id = id_pools['IdentityPools'][0]['IdentityPoolId']

if identity_pool_id:
    print(f"Identity Pool ID: {identity_pool_id}")
    pool_details = cognito_id.describe_identity_pool(IdentityPoolId=identity_pool_id)
    
    # Update Identity Pool to add User Pool provider
    providers = pool_details.get('CognitoIdentityProviders', [])
    providers.append({
        'ProviderName': f"cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
        'ClientId': client_id,
        'ServerSideTokenCheck': False
    })
    
    pool_details['CognitoIdentityProviders'] = providers
    
    if 'ResponseMetadata' in pool_details:
        del pool_details['ResponseMetadata']
        
    # Update identity pool
    cognito_id.update_identity_pool(**pool_details)
    print("Identity Pool updated successfully.")
else:
    print("Could not find any Identity Pool!")

with open("cognito_output.txt", "w") as f:
    f.write(f"USER_POOL_ID={user_pool_id}\n")
    f.write(f"CLIENT_ID={client_id}\n")
    f.write(f"DOMAIN={domain_prefix}\n")
    if identity_pool_id:
        f.write(f"IDENTITY_POOL_ID={identity_pool_id}\n")

print("Setup script finished.")
