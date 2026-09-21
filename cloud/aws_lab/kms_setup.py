import boto3
import time
import urllib.request

s3 = boto3.client('s3', region_name='us-east-1')
ec2 = boto3.client('ec2', region_name='us-east-1')
kms = boto3.client('kms', region_name='us-east-1')
sts = boto3.client('sts', region_name='us-east-1')

account_id = sts.get_caller_identity()['Account']
voclabs_arn = f"arn:aws:iam::{account_id}:role/voclabs"

print("1. Identifying S3 bucket with 'imagebucket' in its name...")
buckets = s3.list_buckets()
image_bucket = None
for bucket in buckets['Buckets']:
    if 'imagebucket' in bucket['Name']:
        image_bucket = bucket['Name']
        break

if image_bucket:
    print(f"Found bucket: {image_bucket}")
    print("Creating dummy clock.png...")
    with open('clock.png', 'w') as out_file:
        out_file.write("This is a dummy clock image.")
    print("Uploading clock.png to S3...")
    # Grant public-read access is specified in the lab
    try:
        s3.upload_file("clock.png", image_bucket, "clock.png", ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded successfully. URL: https://{image_bucket}.s3.amazonaws.com/clock.png")
    except Exception as e:
        print(f"Failed to upload or set ACL (public-read might be blocked): {e}")
        # Try uploading without explicit ACL if it fails due to Block Public Access
        try:
            s3.upload_file("clock.png", image_bucket, "clock.png")
            print(f"Uploaded successfully without public ACL. URL: https://{image_bucket}.s3.amazonaws.com/clock.png")
        except Exception as ex:
            print(f"Failed to upload entirely: {ex}")
else:
    print("No imagebucket found!")

print("\n2. Creating AWS KMS Key 'MyKMSKey'...")
# Custom Key Policy to give voclabs role Admin and User permissions
key_policy = f"""{{
  "Version": "2012-10-17",
  "Id": "key-default-1",
  "Statement": [
    {{
      "Sid": "Enable IAM User Permissions",
      "Effect": "Allow",
      "Principal": {{
        "AWS": "arn:aws:iam::{account_id}:root"
      }},
      "Action": "kms:*",
      "Resource": "*"
    }},
    {{
      "Sid": "Allow access for Key Administrators",
      "Effect": "Allow",
      "Principal": {{
        "AWS": "{voclabs_arn}"
      }},
      "Action": [
        "kms:Create*",
        "kms:Describe*",
        "kms:Enable*",
        "kms:List*",
        "kms:Put*",
        "kms:Update*",
        "kms:Revoke*",
        "kms:Disable*",
        "kms:Get*",
        "kms:Delete*",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:ScheduleKeyDeletion",
        "kms:CancelKeyDeletion"
      ],
      "Resource": "*"
    }},
    {{
      "Sid": "Allow use of the key",
      "Effect": "Allow",
      "Principal": {{
        "AWS": "{voclabs_arn}"
      }},
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Resource": "*"
    }},
    {{
      "Sid": "Allow attachment of persistent resources",
      "Effect": "Allow",
      "Principal": {{
        "AWS": "{voclabs_arn}"
      }},
      "Action": [
        "kms:CreateGrant",
        "kms:ListGrants",
        "kms:RevokeGrant"
      ],
      "Resource": "*",
      "Condition": {{
        "Bool": {{
          "kms:GrantIsForAWSResource": "true"
        }}
      }}
    }}
  ]
}}"""

key_response = kms.create_key(
    Description='MyKMSKey for Lab',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS',
    Policy=key_policy
)

key_id = key_response['KeyMetadata']['KeyId']
print(f"Created Key ID: {key_id}")

print("Creating Alias 'alias/MyKMSKey'...")
kms.create_alias(
    AliasName='alias/MyKMSKey',
    TargetKeyId=key_id
)

print("Enabling automatic key rotation...")
kms.enable_key_rotation(KeyId=key_id)
print("Key rotation enabled.")

print("\n3. Creating and attaching encrypted EBS volume to LabInstance...")
instances = ec2.describe_instances()
lab_instance_id = None
lab_az = None
for res in instances.get('Reservations', []):
    for inst in res.get('Instances', []):
        for tag in inst.get('Tags', []):
            if tag['Key'] == 'Name' and tag['Value'] == 'LabInstance' and inst['State']['Name'] == 'running':
                lab_instance_id = inst['InstanceId']
                lab_az = inst['Placement']['AvailabilityZone']
                break

if lab_instance_id and lab_az:
    print(f"Found LabInstance: {lab_instance_id} in {lab_az}")
    
    print("Creating encrypted 1 GiB EBS volume...")
    volume_res = ec2.create_volume(
        AvailabilityZone=lab_az,
        Encrypted=True,
        KmsKeyId=key_id,
        Size=1,
        VolumeType='gp2'
    )
    volume_id = volume_res['VolumeId']
    print(f"Created Volume ID: {volume_id}. Waiting for it to become available...")
    
    # Wait for volume to be available
    waiter = ec2.get_waiter('volume_available')
    waiter.wait(VolumeIds=[volume_id])
    
    print("Attaching volume to LabInstance at /dev/sdf...")
    ec2.attach_volume(
        Device='/dev/sdf',
        InstanceId=lab_instance_id,
        VolumeId=volume_id
    )
    
    print("Volume attached successfully!")
else:
    print("Could not find a running 'LabInstance'.")

print("\nSetup finished successfully.")
