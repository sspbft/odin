import boto3

ec2 = boto3.client('ec2')

filters = [{"Name": "instance-state-name", "Values": ["running"]}]

def get_ec2_instances(count):
    reservations = ec2.describe_instances(Filters=filters)['Reservations']
    # if len(instances) < count:
    #     raise ValueError("Not enough EC2 instances available on AWS, add more")

    nodes = []
    for r in reservations:
        for instance in r["Instances"]:
            nodes.append({
                "public_hostname": instance["PublicDnsName"],
                "public_ip": instance["PublicIpAddress"],
                "private_hostname": instance["PrivateDnsName"],
                "private_ip": instance["PrivateIpAddress"],
            })

    return nodes
