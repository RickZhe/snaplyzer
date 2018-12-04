import boto3
import click

session = boto3.Session(profile_name='snaplyzer')
ec2 = session.resource('ec2')

def filter_instances(project):
    
    instances = []

    if project:
        filters = [{'Name': 'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

# adding group command when running the script
@click.group()
def instances():
    """Commands for Instances"""

# create the click command 'list'
@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    #calling the function previously define
    instances = filter_instances(project)

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

@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"
    #calling the function previously define}
    instances = filter_instances(project)
    
    # stop() is the actual command to stop an instances.
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return



@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')
def start_instances(project):
    "Start EC2 instances"
    #calling the function previously define}
    instances = filter_instances(project)
    # start() is the actual command to start an instances.
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return

# as best practice to see if there's an imported function 
if __name__ == '__main__':
    instances()