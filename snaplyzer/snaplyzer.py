import boto3
import click

session = boto3.Session(profile_name='snaplyzer')
ec2 = session.resource('ec2')

@click.command()
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    # dock strings.
    "List EC2 instances"
    instances = []

    if project:
        filters = [{'Name': 'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        #adding tags to our variables
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            # the attribue name is from the boto3 documentation https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance 
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
            ## adding tag to our list


    return
# as best practice to see if there's an imported function 
if __name__ == '__main__':
    list_instances()