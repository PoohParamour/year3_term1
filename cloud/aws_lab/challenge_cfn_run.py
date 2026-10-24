import boto3
import time
import os
import subprocess
import urllib.request
import zipfile
import mimetypes

region_east = 'us-east-1'
region_west = 'us-west-2'

cfn_east = boto3.client('cloudformation', region_name=region_east)
cfn_west = boto3.client('cloudformation', region_name=region_west)
ec2_east = boto3.client('ec2', region_name=region_east)
ec2_west = boto3.client('ec2', region_name=region_west)
s3 = boto3.client('s3', region_name=region_east)
pipeline = boto3.client('codepipeline', region_name=region_east)

def separator(title):
    print("\n" + "="*65)
    print(f" {title}")
    print("="*65)

def wait_stack(cfn_client, stack_name, target_status, fail_statuses=None):
    if fail_statuses is None:
        fail_statuses = ['CREATE_FAILED', 'ROLLBACK_COMPLETE', 'ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_FAILED']
    print(f"Waiting for stack '{stack_name}' to reach {target_status}...")
    while True:
        try:
            res = cfn_client.describe_stacks(StackName=stack_name)
            status = res['Stacks'][0]['StackStatus']
            print(f"  [{stack_name}] status: {status}")
            if status == target_status:
                print(f"Stack '{stack_name}' reached {target_status} successfully!")
                return res['Stacks'][0]
            if status in fail_statuses:
                reason = res['Stacks'][0].get('StackStatusReason', 'No reason given')
                raise Exception(f"Stack '{stack_name}' entered {status}: {reason}")
        except Exception as e:
            if target_status == 'DELETE_COMPLETE' and 'does not exist' in str(e):
                return None
            if target_status != 'DELETE_COMPLETE' and 'does not exist' not in str(e):
                raise e
        time.sleep(10)

def wait_pipeline(pipeline_name, expected_commit_id=None):
    print(f"Waiting for pipeline '{pipeline_name}' to execute" + (f" (commit {expected_commit_id[:7]})..." if expected_commit_id else "..."))
    for attempt in range(60):
        try:
            state = pipeline.get_pipeline_state(name=pipeline_name)
            source_rev = None
            for s in state['stageStates']:
                if s['stageName'] == 'Source':
                    for a in s.get('actionStates', []):
                        source_rev = a.get('currentRevision', {}).get('revisionId')
            
            deploy_status = None
            deploy_err = None
            for s in state['stageStates']:
                if s['stageName'] == 'Deploy':
                    for a in s.get('actionStates', []):
                        deploy_status = a.get('latestExecution', {}).get('status')
                        deploy_err = a.get('latestExecution', {}).get('errorDetails', {}).get('message')
            
            print(f"  [{pipeline_name}] Source rev: {source_rev[:7] if source_rev else 'none'}, Deploy action: {deploy_status}")
            
            if expected_commit_id and source_rev != expected_commit_id:
                print(f"  Waiting for pipeline to pick up commit {expected_commit_id[:7]}...")
                time.sleep(10)
                continue
                
            if deploy_status == 'Succeeded':
                print(f"Pipeline '{pipeline_name}' Deploy action SUCCEEDED!")
                return True
            if deploy_status in ['Failed', 'Cancelled']:
                raise Exception(f"Pipeline '{pipeline_name}' Deploy action {deploy_status}! Error: {deploy_err}")
        except Exception as e:
            if "Pipeline" in str(e) and "Deploy action" in str(e):
                raise e
            print(f"  Checking pipeline: {e}")
        time.sleep(10)
    raise Exception(f"Pipeline '{pipeline_name}' timed out.")

def run_git(args, cwd):
    cmd = ['git'] + args
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise Exception(f"Git command failed: {' '.join(cmd)}\nError: {res.stderr}")
    return res.stdout.strip()

def get_current_commit_id(cwd):
    res = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=cwd, stdout=subprocess.PIPE, text=True)
    return res.stdout.strip()

def main():
    repo_dir = os.path.abspath('CFTemplatesRepo')

    # =============================================================
    # CHALLENGE 1: S3 Static Website with CloudFormation
    # =============================================================
    separator("CHALLENGE 1: S3 Static Website (Task 2 & 3)")

    # Task 2: Create S3.yaml
    s3_yaml_path = 'S3.yaml'
    s3_initial_content = """AWSTemplateFormatVersion: "2010-09-09"
Description: cafe S3 template

Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
"""
    with open(s3_yaml_path, 'w') as f:
        f.write(s3_initial_content)
    print("Created initial S3.yaml")

    # Deploy CreateBucket stack
    try:
        stack = cfn_east.describe_stacks(StackName='CreateBucket')
        print(f"Stack 'CreateBucket' already exists ({stack['Stacks'][0]['StackStatus']})")
    except Exception:
        print("Creating stack 'CreateBucket'...")
        cfn_east.create_stack(StackName='CreateBucket', TemplateBody=s3_initial_content)
    
    wait_stack(cfn_east, 'CreateBucket', 'CREATE_COMPLETE')
    
    # Get bucket name
    res = cfn_east.describe_stack_resources(StackName='CreateBucket')
    bucket_name = None
    for r in res['StackResources']:
        if r['LogicalResourceId'] == 'S3Bucket':
            bucket_name = r['PhysicalResourceId']
    print(f"Created S3 Bucket Name: {bucket_name}")

    # Task 3: Extract static website assets and upload
    print("\nExtracting static-website.zip...")
    if not os.path.exists("static"):
        with zipfile.ZipFile("static-website.zip", 'r') as zip_ref:
            zip_ref.extractall("static")
    print("Extracted static-website to static/")

    print(f"Configuring bucket ownership and public access on {bucket_name}...")
    s3.put_bucket_ownership_controls(
        Bucket=bucket_name,
        OwnershipControls={'Rules': [{'ObjectOwnership': 'BucketOwnerPreferred'}]}
    )
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )

    print(f"Uploading files to s3://{bucket_name}/...")
    for root, dirs, files in os.walk("static"):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, "static")
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type is None:
                content_type = 'binary/octet-stream'
            extra_args = {'ACL': 'public-read', 'ContentType': content_type}
            s3.upload_file(full_path, bucket_name, rel_path, ExtraArgs=extra_args)
    print("Upload completed successfully.")

    # Update S3.yaml with DeletionPolicy, WebsiteConfiguration, Outputs
    s3_updated_content = """AWSTemplateFormatVersion: "2010-09-09"
Description: cafe S3 template

Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      WebsiteConfiguration:
        IndexDocument: index.html

Outputs:
  WebsiteURL:
    Value: !GetAtt S3Bucket.WebsiteURL
    Description: URL for website hosted on S3
"""
    with open(s3_yaml_path, 'w') as f:
        f.write(s3_updated_content)

    print("Validating updated S3.yaml...")
    cfn_east.validate_template(TemplateBody=s3_updated_content)

    print("Updating stack 'CreateBucket'...")
    try:
        cfn_east.update_stack(StackName='CreateBucket', TemplateBody=s3_updated_content)
        wait_stack(cfn_east, 'CreateBucket', 'UPDATE_COMPLETE')
    except Exception as e:
        if "No updates are to be performed" in str(e):
            print("Stack 'CreateBucket' already up to date.")
        else:
            raise e

    res = cfn_east.describe_stacks(StackName='CreateBucket')
    website_url = None
    for out in res['Stacks'][0].get('Outputs', []):
        if out['OutputKey'] == 'WebsiteURL':
            website_url = out['OutputValue']
    print(f"S3 Static Website URL: {website_url}")

    # =============================================================
    # CHALLENGE 3: Network & App Layers via CodePipeline
    # =============================================================
    separator("CHALLENGE 3: Network Layer (Task 5)")

    network_yaml_path = os.path.join(repo_dir, 'templates', 'cafe-network.yaml')
    with open(os.path.join(repo_dir, 'templates', 'template1.yaml'), 'r') as f:
        net_content = f.read()
    
    net_content = net_content.replace("Description:", "Description: Network layer for the cafe")
    with open(network_yaml_path, 'w') as f:
        f.write(net_content)
    
    print("Committing and pushing initial cafe-network.yaml...")
    run_git(['add', 'templates/cafe-network.yaml'], repo_dir)
    try:
        run_git(['commit', '-m', 'initial commit of network template'], repo_dir)
        run_git(['push', 'origin', 'main'], repo_dir)
    except Exception as e:
        print(f"Note on git commit/push: {e}")

    commit_net_1 = get_current_commit_id(repo_dir)
    print(f"Commit ID: {commit_net_1}")

    print("Waiting for CafeNetworkPipeline to deploy update-cafe-network...")
    wait_pipeline('CafeNetworkPipeline', commit_net_1)
    wait_stack(cfn_east, 'update-cafe-network', 'CREATE_COMPLETE')

    # Task 6: Add Outputs to cafe-network.yaml
    separator("Task 6: Adding Outputs to cafe-network.yaml")
    outputs_block = """
Outputs:
  PublicSubnet:
    Description: The subnet ID to use for public web servers
    Value:
      Ref: PublicSubnet
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-SubnetID'
  VpcId:
    Description: The VPC ID
    Value:
      Ref: VPC
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-VpcID'
"""
    with open(network_yaml_path, 'w') as f:
        f.write(net_content + outputs_block)

    print("Committing and pushing updated cafe-network.yaml with outputs...")
    run_git(['add', 'templates/cafe-network.yaml'], repo_dir)
    try:
        run_git(['commit', '-m', 'add outputs to network template'], repo_dir)
        run_git(['push', 'origin', 'main'], repo_dir)
    except Exception as e:
        print(f"Note on git commit/push: {e}")

    commit_net_2 = get_current_commit_id(repo_dir)
    print(f"Commit ID: {commit_net_2}")

    print("Waiting for CafeNetworkPipeline to update update-cafe-network...")
    wait_pipeline('CafeNetworkPipeline', commit_net_2)
    wait_stack(cfn_east, 'update-cafe-network', 'UPDATE_COMPLETE')

    # Task 7: cafe-app.yaml
    separator("Task 7: Creating cafe-app.yaml & Deploying Application Stack")
    app_yaml_path = os.path.join(repo_dir, 'templates', 'cafe-app.yaml')

    cafe_app_full = """AWSTemplateFormatVersion: 2010-09-09
Description: Cafe application

Parameters:

  LatestAmiId:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'

  CafeNetworkParameter:
    Type: String
    Default: update-cafe-network

  InstanceType:
    Description: WebServer EC2 instance type
    Type: String
    Default: t2.small
    AllowedValues:
      - t2.micro
      - t2.small
      - t3.micro
      - t3.small

Mappings:

  RegionMap:
    us-east-1:
      "keypair": "vockey"
    us-west-2:
      "keypair": "cafe-oregon"

Resources:

  CafeSG:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: Enable SSH, HTTP access
      VpcId: !ImportValue
        'Fn::Sub': '${CafeNetworkParameter}-VpcID'
      Tags:
        - Key: Name
          Value: CafeSG
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '80'
          ToPort: '80'
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: '22'
          ToPort: '22'
          CidrIp: 0.0.0.0/0

  CafeInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: !Ref InstanceType
      KeyName: !FindInMap [RegionMap, !Ref "AWS::Region", keypair]
      IamInstanceProfile: CafeRole
      NetworkInterfaces:
        - DeviceIndex: '0'
          AssociatePublicIpAddress: 'true'
          SubnetId: !ImportValue
            'Fn::Sub': '${CafeNetworkParameter}-SubnetID'
          GroupSet:
            - !Ref CafeSG
      Tags:
        - Key: Name
          Value: Cafe Web Server
      UserData:
        Fn::Base64:
          !Sub |
            #!/bin/bash
            yum -y update
            yum install -y httpd mariadb-server wget
            amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
            systemctl enable httpd
            systemctl start httpd
            systemctl enable mariadb
            systemctl start mariadb
            wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACACAD-3-113230/15-lab-mod11-challenge-CFn/s3/cafe-app.sh
            chmod +x cafe-app.sh
            ./cafe-app.sh

Outputs:
  WebServerPublicIP:
    Value: !GetAtt 'CafeInstance.PublicIp'
"""

    with open(app_yaml_path, 'w') as f:
        f.write(cafe_app_full)

    print("Validating cafe-app.yaml...")
    cfn_east.validate_template(TemplateBody=cafe_app_full)

    print("Committing and pushing cafe-app.yaml...")
    run_git(['add', 'templates/cafe-app.yaml'], repo_dir)
    try:
        run_git(['commit', '-m', 'add application template'], repo_dir)
        run_git(['push', 'origin', 'main'], repo_dir)
    except Exception as e:
        print(f"Note on git commit/push: {e}")

    commit_app = get_current_commit_id(repo_dir)
    print(f"Commit ID: {commit_app}")

    print("Waiting for CafeAppPipeline to deploy update-cafe-app...")
    wait_pipeline('CafeAppPipeline', commit_app)
    app_stack_east = wait_stack(cfn_east, 'update-cafe-app', 'CREATE_COMPLETE')

    app_east_ip = None
    for out in app_stack_east.get('Outputs', []):
        if out['OutputKey'] == 'WebServerPublicIP':
            app_east_ip = out['OutputValue']
    print(f"us-east-1 Cafe Web Server IP: {app_east_ip}")
    print(f"Website URL: http://{app_east_ip}/cafe")

    # =============================================================
    # CHALLENGE 4: Duplicating to us-west-2 (Task 7 in doc)
    # =============================================================
    separator("CHALLENGE 4: Duplicating to us-west-2 (Oregon)")

    # 1. Deploy update-cafe-network in us-west-2
    with open(network_yaml_path, 'r') as f:
        net_yaml_content = f.read()

    try:
        stack = cfn_west.describe_stacks(StackName='update-cafe-network')
        print(f"us-west-2 'update-cafe-network' status: {stack['Stacks'][0]['StackStatus']}")
    except Exception:
        print("Creating stack 'update-cafe-network' in us-west-2...")
        cfn_west.create_stack(
            StackName='update-cafe-network',
            TemplateBody=net_yaml_content
        )
    wait_stack(cfn_west, 'update-cafe-network', 'CREATE_COMPLETE')

    # 2. Create KeyPair cafe-oregon in us-west-2
    print("Checking EC2 Key Pair 'cafe-oregon' in us-west-2...")
    kps = ec2_west.describe_key_pairs(Filters=[{'Name': 'key-name', 'Values': ['cafe-oregon']}])
    if not kps['KeyPairs']:
        print("Creating key pair 'cafe-oregon' in us-west-2...")
        ec2_west.create_key_pair(KeyName='cafe-oregon')
    else:
        print("Key pair 'cafe-oregon' already exists in us-west-2.")

    # 3. Upload cafe-app.yaml to repobucket
    s3_buckets = s3.list_buckets()['Buckets']
    repo_bucket_name = None
    for b in s3_buckets:
        if 'repobucket' in b['Name']:
            repo_bucket_name = b['Name']
            break
    print(f"Found RepoBucket: {repo_bucket_name}")

    print(f"Uploading cafe-app.yaml to s3://{repo_bucket_name}/cafe-app.yaml...")
    s3.upload_file(app_yaml_path, repo_bucket_name, 'cafe-app.yaml')
    s3_obj_url = f"https://{repo_bucket_name}.s3.amazonaws.com/cafe-app.yaml"
    print(f"Template S3 URL: {s3_obj_url}")

    # 4. Create application stack in us-west-2
    print("Creating stack 'update-cafe-app' in us-west-2 with InstanceType=t3.micro...")
    try:
        stack = cfn_west.describe_stacks(StackName='update-cafe-app')
        print(f"us-west-2 'update-cafe-app' status: {stack['Stacks'][0]['StackStatus']}")
    except Exception:
        cfn_west.create_stack(
            StackName='update-cafe-app',
            TemplateURL=s3_obj_url,
            Parameters=[
                {'ParameterKey': 'InstanceType', 'ParameterValue': 't3.micro'},
                {'ParameterKey': 'CafeNetworkParameter', 'ParameterValue': 'update-cafe-network'}
            ],
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
        )
    app_stack_west = wait_stack(cfn_west, 'update-cafe-app', 'CREATE_COMPLETE')

    app_west_ip = None
    for out in app_stack_west.get('Outputs', []):
        if out['OutputKey'] == 'WebServerPublicIP':
            app_west_ip = out['OutputValue']
    print(f"us-west-2 Cafe Web Server IP: {app_west_ip}")
    print(f"Website URL: http://{app_west_ip}/cafe")

    separator("CHALLENGE LAB COMPLETED SUCCESSFULLY!")
    print(f"1. Static Website S3 URL: {website_url}")
    print(f"2. us-east-1 Cafe App URL: http://{app_east_ip}/cafe")
    print(f"3. us-west-2 Cafe App URL: http://{app_west_ip}/cafe")

if __name__ == '__main__':
    main()
