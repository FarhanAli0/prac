import boto3
import json
import time
import os
       
session = boto3.Session(
       
aws_access_key_id='ASIAZRVBTTD7FTMMK5NS',
aws_secret_access_key='4L4p12An4We56yiRXGZCc3gfkCnqvaYi8+GQjuA2',
aws_session_token='FwoGZXIvYXdzEDYaDFjoYd21j441+VV7lyKoAR2qK2foPOZWfyMFwNsb/cvi2VeCUPu1ikDk74S9HP9HAsjnIpZpeMbXWzKEu2Op+iqplgSrycY1akRckrfTepCXeJnVu6AlfwcCT08Axp8x7hfb95za7KD2Jp6rR45/+83JwxI0l5yUze1D14QFES0dgj75RoVRxLUZ/REimMCXBpifQpXo8G5SoKm8Hj+IWJPD0dphBM9kroyQU8S/Abh0QjqFi5fxrCjS2JqfBjItNqwkqoTDoScINU1SIbvcIXhY9c+Ck5+nkIXd+3wUGZSfmVHwMgATaqSUH+K5'
)
# Connect to EC2
ec2_client = session.client('ec2', region_name='us-east-1')

# Connect to S3
s3_client = session.client('s3', region_name='us-east-1')

def retrieve_data():
    # Get list of all EC2 instances
    instances = ec2_client.describe_instances()

    # Create empty list to store instance data
    instance_list = []

    # Iterate over instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_dict = {}
            instance_dict['instance_id'] = instance['InstanceId']
            instance_dict['tags'] = instance['Tags']
            instance_list.append(instance_dict)

    # Get list of all S3 Buckets
    buckets = s3_client.list_buckets()

    # Create empty list to store bucket data
    bucket_list = []

    # Iterate over buckets
    for bucket in buckets['Buckets']:
        bucket_dict = {}
        bucket_dict['bucket_name'] = bucket['Name']
        bucket_list.append(bucket_dict)

    # Combine instance and bucket lists
    data = {'instance_list': instance_list, 'bucket_list': bucket_list}

    # Write data to JSON file
    with open("input.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    
# Retrieve data every 24 hours
while True:
    retrieve_data()
    time.sleep(24 * 60 * 60)