import boto3
import os
import uuid


# Setup boto3
S3API = boto3.client("s3", region_name="us-east-1")
EC2API = boto3.client("ec2", region_name="us-east-1")
CFRONTAPI = boto3.client("cloudfront", region_name="us-east-1")
CFORMATION = boto3.client("cloudformation", region_name="us-east-1")

# Copy website code to S3
buckets = S3API.list_buckets()
website_bucket = buckets['Buckets'][0]['Name']
print('The website S3 bucket is:', website_bucket)

os.chdir('/Users/pattarapol/itkmitl/year3_term1/cloud/aws_lab')
os.system('aws s3 cp website s3://%s --recursive --cache-control "max-age=0"' %website_bucket)

# Get Cloud9 ec2 instance info needed for next steps
get_ec2_instances = EC2API.describe_instances()
for ec2_reservation in get_ec2_instances['Reservations']:
    for ec2_instance in ec2_reservation['Instances']:
        if ec2_instance['State']['Name'] == 'running':
            ec2_pub_dns = ec2_instance['PublicDnsName']
            ec2_sec_grp_id = ec2_instance['SecurityGroups'][0]['GroupId']

# Add Security Group rule the the Cloud9 ec2 Security Group
# tcp 8080 0.0.0.0/0
try:
    add_sec_grp_rule = EC2API.authorize_security_group_ingress(GroupId=ec2_sec_grp_id,FromPort=8080,ToPort=8080,IpProtocol='tcp',CidrIp='0.0.0.0/0')
    if len(add_sec_grp_rule['SecurityGroupRules']) != 0:
        print('Added security group rule.')
    else:
        print('There was a problem adding the security group rule.')
except:
    print('There was a problem adding the security group rule. If you have already run this script, the rule was already added.')


# Get required information to deploy CloudFront
cfront_caller_ref = str(uuid.uuid4())
cloudfront_oais = CFRONTAPI.list_cloud_front_origin_access_identities()


#Checking for dnagling OAI and removing if it exists
if len(cloudfront_oais['CloudFrontOriginAccessIdentityList']['Items']) > 1:
    print('More than 1 OAI was found. Cleaning up old OAI.')
    
    get_stacks = CFORMATION.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE'
            ]
        )
    
    #print(get_stacks['StackSummaries'])
    
    #Get ID for the stack that was created from the lab.template.
    #There will be a second one associated with Cloud9.
    stack_name = ''
    keep_oai = ''
    for stack_summary in get_stacks['StackSummaries']:
        if 'Cloud9' not in stack_summary['StackName']:
            stack_name = stack_summary['StackName']
        
    get_stack_resources = CFORMATION.list_stack_resources(
                                StackName=stack_name
                            )
    
    for resource_summary in get_stack_resources['StackResourceSummaries']:
        if resource_summary['LogicalResourceId'] == 'BirdAppOAI':
            keep_oai = resource_summary['PhysicalResourceId']
            
    
    delete_oai = ''
    
    for item in cloudfront_oais['CloudFrontOriginAccessIdentityList']['Items']:
        if item['Id'] != keep_oai:
            delete_oai = item['Id']
            oai_conf = CFRONTAPI.get_cloud_front_origin_access_identity_config(
                            Id=delete_oai
                        )
            etag = oai_conf['ETag']
            remove_oai = CFRONTAPI.delete_cloud_front_origin_access_identity(
                            Id=delete_oai,
                            IfMatch=etag
                        )
    
    if remove_oai['ResponseMetadata']['HTTPStatusCode'] == 204:
        print('Old OAI successfully removed')
    else:
        print('There was a problem removing the old OAI.')


cf_oai = cloudfront_oais['CloudFrontOriginAccessIdentityList']['Items'][0]['Id']
print('The Origin Access Id is:', cf_oai)

# Create CloudFront distribution
# two origins
# default behavior
# two custom behaviors
check_for_distributions = CFRONTAPI.list_distributions()
if check_for_distributions['DistributionList']['Quantity'] == 0:

    create_distribution = CFRONTAPI.create_distribution(
                        DistributionConfig={
                            'CallerReference': cfront_caller_ref,
                            'Aliases': {'Quantity': 0},
                            'DefaultRootObject': 'index.html', 
                            'Origins': {
                                'Quantity': 2,
                                'Items': [
                                    {
                                        'Id': ec2_pub_dns, 
                                        'DomainName': ec2_pub_dns, 
                                        'OriginPath': '', 
                                        'CustomHeaders': {'Quantity': 0}, 
                                        'CustomOriginConfig': {
                                            'HTTPPort': 8080, 
                                            'HTTPSPort': 443,
                                            'OriginProtocolPolicy': 'http-only', 
                                            'OriginSslProtocols': {
                                                'Quantity': 3, 'Items': ['TLSv1', 'TLSv1.1', 'TLSv1.2']
                                            }, 
                                        'OriginReadTimeout': 30, 
                                        'OriginKeepaliveTimeout': 5
                                    }, 
                                        'ConnectionAttempts': 3, 
                                        'ConnectionTimeout': 10, 
                                        'OriginShield': {'Enabled': False}
                                    },
                                    {
                                        'Id': 'S3-birdsOrigin', 
                                        'DomainName': website_bucket + '.s3.amazonaws.com', 
                                        'OriginPath': '', 
                                        'CustomHeaders': {'Quantity': 0}, 
                                        'S3OriginConfig':  
                                            {
                                                'OriginAccessIdentity': 'origin-access-identity/cloudfront/' + cf_oai
                                            }, 
                                        'ConnectionAttempts': 3, 
                                        'ConnectionTimeout': 10, 
                                        'OriginShield': {'Enabled': False}
                                    }
                                ]
                            },
                            'OriginGroups': {'Quantity': 0}, 
                            'DefaultCacheBehavior': {
                                'TargetOriginId': 'S3-birdsOrigin', 
                                'TrustedSigners': {'Enabled': False, 'Quantity': 0}, 
                                'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0}, 
                                'ViewerProtocolPolicy': 'redirect-to-https',
                                'AllowedMethods': {
                                    'Quantity': 2, 
                                    'Items': ['HEAD', 'GET'], 
                                    'CachedMethods': {
                                        'Quantity': 2, 
                                        'Items': ['HEAD', 'GET']}
                                    }, 
                                'SmoothStreaming': False, 
                                'Compress': True, 
                                'LambdaFunctionAssociations': {'Quantity': 0},
                                'FunctionAssociations': {'Quantity': 0}, 
                                'FieldLevelEncryptionId': '', 
                                'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad'
                            },
                            'CacheBehaviors': {
                                'Quantity': 3, 
                                'Items': [
                                    {'PathPattern': '/sightings', 
                                    'TargetOriginId': ec2_pub_dns, 
                                    'TrustedSigners': {'Enabled': False, 'Quantity': 0}, 
                                    'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0}, 
                                    'ViewerProtocolPolicy': 'allow-all', 
                                    'AllowedMethods': {
                                        'Quantity': 7, 
                                        'Items': ['HEAD', 'DELETE', 'POST', 'GET', 'OPTIONS', 'PUT', 'PATCH'], 
                                        'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
                                    }, 
                                    'SmoothStreaming': False, 
                                    'Compress': True, 
                                    'LambdaFunctionAssociations': {'Quantity': 0}, 
                                    'FunctionAssociations': {'Quantity': 0}, 
                                    'FieldLevelEncryptionId': '', 
                                    'ForwardedValues': {
                                        'QueryString': False, 
                                        'Cookies': {'Forward': 'none'}, 
                                        'Headers': {
                                            'Quantity': 6, 
                                            'Items': ['Origin', 'Authorization', 'Access-Control-Request-Method', 'Access-Control-Request-Headers', 'Referer', 'Host']
                                        }, 
                                    'QueryStringCacheKeys': {'Quantity': 0}
                                    }, 
                                    'MinTTL': 0, 
                                    'DefaultTTL': 86400, 
                                    'MaxTTL': 31536000}, 
                                    {'PathPattern': '/report-sightings', 
                                    'TargetOriginId': ec2_pub_dns, 
                                    'TrustedSigners': {'Enabled': False, 'Quantity': 0}, 
                                    'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0}, 
                                    'ViewerProtocolPolicy': 'allow-all', 
                                    'AllowedMethods': {
                                        'Quantity': 7, 
                                        'Items': ['HEAD', 'DELETE', 'POST', 'GET', 'OPTIONS', 'PUT', 'PATCH'], 
                                        'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
                                    }, 
                                    'SmoothStreaming': False, 
                                    'Compress': True, 
                                    'LambdaFunctionAssociations': {'Quantity': 0}, 
                                    'FunctionAssociations': {'Quantity': 0}, 
                                    'FieldLevelEncryptionId': '', 
                                    'ForwardedValues': {'QueryString': False, 
                                    'Cookies': {'Forward': 'none'}, 
                                    'Headers': {
                                        'Quantity': 6, 
                                        'Items': ['Authorization', 'Origin', 'Access-Control-Request-Method', 'Access-Control-Request-Headers', 'Referer', 'Host']
                                    }, 
                                    'QueryStringCacheKeys': {'Quantity': 0}}, 
                                    'MinTTL': 0, 
                                    'DefaultTTL': 86400, 
                                    'MaxTTL': 31536000},
                                    {'PathPattern': '/siteadmin', 
                                    'TargetOriginId': ec2_pub_dns, 
                                    'TrustedSigners': {'Enabled': False, 'Quantity': 0}, 
                                    'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0}, 
                                    'ViewerProtocolPolicy': 'allow-all', 
                                    'AllowedMethods': {
                                        'Quantity': 7, 
                                        'Items': ['HEAD', 'DELETE', 'POST', 'GET', 'OPTIONS', 'PUT', 'PATCH'], 
                                        'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
                                    }, 
                                    'SmoothStreaming': False, 
                                    'Compress': True, 
                                    'LambdaFunctionAssociations': {'Quantity': 0}, 
                                    'FunctionAssociations': {'Quantity': 0}, 
                                    'FieldLevelEncryptionId': '', 
                                    'ForwardedValues': {
                                        'QueryString': False, 
                                        'Cookies': {'Forward': 'none'}, 
                                        'Headers': {
                                            'Quantity': 6, 
                                            'Items': ['Origin', 'Authorization', 'Access-Control-Request-Method', 'Access-Control-Request-Headers', 'Referer', 'Host']
                                        }, 
                                    'QueryStringCacheKeys': {'Quantity': 0}
                                    }, 
                                    'MinTTL': 0, 
                                    'DefaultTTL': 86400, 
                                    'MaxTTL': 31536000}
                                ]
                            }, 
                            'CustomErrorResponses': {
                                'Quantity': 1, 
                                'Items': [{'ErrorCode': 404, 'ResponsePagePath': '/', 'ResponseCode': '200', 'ErrorCachingMinTTL': 30}]
                            }, 
                            'Comment': '', 
                            'Logging': {'Enabled': False, 'IncludeCookies': False, 'Bucket': '', 'Prefix': ''}, 
                            'PriceClass': 'PriceClass_All',
                            'Enabled': True, 
                            'ViewerCertificate': {
                                'CloudFrontDefaultCertificate': True, 
                                'MinimumProtocolVersion': 'TLSv1', 
                                'CertificateSource': 'cloudfront'}, 
                            'Restrictions': {
                                'GeoRestriction': {'RestrictionType': 'none', 'Quantity': 0}
                            }, 
                            'WebACLId': '', 
                            'HttpVersion': 'http2', 
                            'IsIPV6Enabled': True})
else:
    print("You must be rerunning the script. A CloudFront distribution already exists. We won't create a new one.")