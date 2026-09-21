import boto3
import time

asg = boto3.client('autoscaling', region_name='us-east-1')
cw = boto3.client('cloudwatch', region_name='us-east-1')

print("Waiting for ASG to scale...")
for i in range(20):
    a = asg.describe_auto_scaling_groups(AutoScalingGroupNames=['Cafe-ASG'])['AutoScalingGroups'][0]
    print(f"Instances: {len(a['Instances'])}, Desired: {a['DesiredCapacity']}")
    if len(a['Instances']) > 2:
        print("Scaled out successfully!")
        break
    time.sleep(15)
