import boto3
import click

session = boto3.Session(profile_name='snaplyzer')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    # dock strings.
    "List EC2 instances"
    for i in ec2.instances.all():
        print(','.join((
            # the attribue name is from the boto3 documentation https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance 
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name)))

    return


# as best practice to see if there's an imported function 
if __name__ == '__main__':
    list_instances()

