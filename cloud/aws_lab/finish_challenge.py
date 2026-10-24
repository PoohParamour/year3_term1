import boto3
import time
import os

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

def wait_pipeline_deploy(pipeline_name):
    print(f"Waiting for pipeline '{pipeline_name}' to complete...")
    for _ in range(60):
        try:
            state = pipeline.get_pipeline_state(name=pipeline_name)
            deploy_status = None
            deploy_err = None
            for s in state['stageStates']:
                if s['stageName'] == 'Deploy':
                    for a in s.get('actionStates', []):
                        deploy_status = a.get('latestExecution', {}).get('status')
                        deploy_err = a.get('latestExecution', {}).get('errorDetails', {}).get('message')
            
            print(f"  [{pipeline_name}] Deploy action status: {deploy_status}")
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

def main():
    separator("Waiting for CafeAppPipeline and update-cafe-app in us-east-1")
    wait_pipeline_deploy('CafeAppPipeline')
    app_stack_east = wait_stack(cfn_east, 'update-cafe-app', 'CREATE_COMPLETE')

    app_east_ip = None
    for out in app_stack_east.get('Outputs', []):
        if out['OutputKey'] == 'WebServerPublicIP':
            app_east_ip = out['OutputValue']
    print(f"us-east-1 Cafe Web Server IP: {app_east_ip}")
    print(f"Website URL: http://{app_east_ip}/cafe")

    # =============================================================
    # CHALLENGE 4: Duplicating to us-west-2 (Oregon)
    # =============================================================
    separator("CHALLENGE 4: Duplicating to us-west-2 (Oregon)")

    # 1. Deploy update-cafe-network in us-west-2
    net_path = os.path.abspath('CFTemplatesRepo/templates/cafe-network.yaml')
    with open(net_path, 'r') as f:
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

    app_path = os.path.abspath('CFTemplatesRepo/templates/cafe-app.yaml')
    print(f"Uploading cafe-app.yaml to s3://{repo_bucket_name}/cafe-app.yaml...")
    s3.upload_file(app_path, repo_bucket_name, 'cafe-app.yaml')
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

    separator("ALL TASKS COMPLETED SUCCESSFULLY!")
    print(f"us-east-1 Cafe App: http://{app_east_ip}/cafe")
    print(f"us-west-2 Cafe App: http://{app_west_ip}/cafe")

if __name__ == '__main__':
    main()
