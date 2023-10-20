import boto3

# Initialize the Boto3 client for the Elastic Load Balancing service
elbv2 = boto3.client('elbv2', region_name='your_aws_region')

# Replace 'your_target_group_arn' with the ARN of your target group
target_group_arn = 'your_target_group_arn'

# Describe the target health of the target group
response = elbv2.describe_target_health(TargetGroupArn=target_group_arn)

# Initialize a list to store unhealthy instance IPs
unhealthy_ips = []

# Initialize the EC2 client to retrieve instance IP addresses
ec2 = boto3.client('ec2', region_name='your_aws_region')

# Iterate through the target health descriptions
for target in response['TargetHealthDescriptions']:
    # Check if the instance is unhealthy
    if target['TargetHealth']['State'] != 'healthy':
        instance_id = target['Target']['Id']
        instance_info = ec2.describe_instances(InstanceIds=[instance_id])
        if 'Reservations' in instance_info and 'Instances' in instance_info['Reservations'][0]:
            instance = instance_info['Reservations'][0]['Instances'][0]
            ip_address = instance['PrivateIpAddress']
            unhealthy_ips.append(ip_address)

# Save the unhealthy instance IPs to a text file
with open('unhealthy_instance_ips.txt', 'w') as file:
    for ip in unhealthy_ips:
        file.write(ip + '\n')
