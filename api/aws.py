import boto3

ec2 = boto3.client('ec2')

filters = [{"Name": "instance-state-name", "Values": ["running"]}]

def get_ec2_instances(count):
    instances = ec2.describe_instances(Filters=filters)['Reservations']
    # if len(instances) < count:
    #     raise ValueError("Not enough EC2 instances available on AWS, add more")

    nodes = []
    for x in instances:
        i = x['Instances'][0]
        nodes.append({
            "hostname": i['PublicDnsName']
        })
    
    return nodes
