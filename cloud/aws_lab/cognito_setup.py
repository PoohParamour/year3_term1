import boto3
import random
import string
import time

cognito = boto3.client('cognito-idp', region_name='us-east-1')
cognito_id = boto3.client('cognito-identity', region_name='us-east-1')

cloudfront_domain = 'd1etr45kvyfa3a.cloudfront.net'

print("Creating User Pool 'bird_app'...")
user_pool_response = cognito.create_user_pool(
    PoolName='bird_app',
    Policies={
        'PasswordPolicy': {
            'MinimumLength': 8,
            'RequireUppercase': True,
            'RequireLowercase': True,
            'RequireNumbers': True,
            'RequireSymbols': True,
        }
    },
    Schema=[
        {
            'Name': 'email',
            'Required': True,
            'Mutable': True
        }
    ]
)

user_pool_id = user_pool_response['UserPool']['Id']
print(f"User Pool ID: {user_pool_id}")

print("Creating App Client 'bird_app_client'...")
client_response = cognito.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName='bird_app_client',
    GenerateSecret=False,
    ExplicitAuthFlows=[
        'ALLOW_USER_PASSWORD_AUTH',
        'ALLOW_REFRESH_TOKEN_AUTH'
    ],
    SupportedIdentityProviders=['COGNITO'],
    CallbackURLs=[f'https://{cloudfront_domain}/callback.html'],
    AllowedOAuthFlows=['code', 'implicit'],
    AllowedOAuthScopes=['email', 'openid'],
    AllowedOAuthFlowsUserPoolClient=True
)

client_id = client_response['UserPoolClient']['ClientId']
print(f"App Client ID: {client_id}")

random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
domain_prefix = f"bird-app-domain-{random_suffix}"

print(f"Creating Cognito Domain '{domain_prefix}'...")
cognito.create_user_pool_domain(
    Domain=domain_prefix,
    UserPoolId=user_pool_id
)

print("Creating user 'testuser'...")
cognito.admin_create_user(
    UserPoolId=user_pool_id,
    Username='testuser',
    UserAttributes=[
        {'Name': 'email', 'Value': 'testuser@example.com'},
        {'Name': 'email_verified', 'Value': 'true'}
    ],
    MessageAction='SUPPRESS',
    TemporaryPassword='Lab-password1$'
)
cognito.admin_set_user_password(
    UserPoolId=user_pool_id,
    Username='testuser',
    Password='Lab-password1$',
    Permanent=True
)

print("Creating user 'admin'...")
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
cognito.admin_set_user_password(
    UserPoolId=user_pool_id,
    Username='admin',
    Password='Admin123$',
    Permanent=True
)

print("Creating group 'Administrators'...")
cognito.create_group(
    GroupName='Administrators',
    UserPoolId=user_pool_id
)

print("Adding 'admin' to 'Administrators'...")
cognito.admin_add_user_to_group(
    UserPoolId=user_pool_id,
    Username='admin',
    GroupName='Administrators'
)

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
