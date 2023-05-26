import boto3

def should_skip_stop(instance):
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'skip_stop' and tag['Value'].lower() == 'true':
            return True
    return False

def shutdown_standalone_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if should_skip_stop(instance):
                print(f"Skipping stopping EC2 instance '{instance['InstanceId']}' due to skip_stop tag")
                continue
            instance_ids.append(instance['InstanceId'])

    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Stopping EC2 instances: {', '.join(instance_ids)}")

def should_skip_stop(asg):
    tags = asg.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'skip_stop' and tag['Value'].lower() == 'true':
            return True
    return False

def scale_down_auto_scaling_groups():
    autoscaling = boto3.client('autoscaling')
    response = autoscaling.describe_auto_scaling_groups()

    for asg in response['AutoScalingGroups']:
        asg_name = asg['AutoScalingGroupName']

        if should_skip_stop(asg):
            print(f"Skipping setting desired count and minimum count to zero for Auto Scaling group '{asg_name}' due to skip_stop tag")
            continue

        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=0,
            DesiredCapacity=0
        )
        print(f"Set desired count and minimum count to zero for Auto Scaling group '{asg_name}'")

def lambda_handler(event, context):
    scale_down_auto_scaling_groups()
    shutdown_standalone_instances()
