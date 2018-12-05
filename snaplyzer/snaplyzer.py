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

#nasted these click groups
@click.group()
def cli():
    """Manage snapshots commands"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 snapshots"
    #calling the function previously define
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return



@cli.group('volumes')
def volumes():
    """Commands for Voluems"""


@volumes.command('list')
@click.option('--project', default=None,
    help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"
    #calling the function previously define
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('instances')
def instances():
    """Commands for Instances"""

@instances.command('snapshot')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Created snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snaplyzer")
        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running() 
    print("Job's done!")
    return

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
    cli()