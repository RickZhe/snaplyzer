import boto3
# import botocore because when instance stops, there's a pending stage where you can't start until it's completely stopped.
#
#        try:
#            i.stop()
#        except botocore.exceptions.ClientError as e:
#            print(" Could not start {0}".format(i.id) + str(e))
#            continue
import botocore
import click

# This is the session configure from 'aws configure --profile snaplyzer'.
# This is critical when other workstation needs to comunnicate with aws.
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

def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

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
@click.option('--all', 'list_all', default=False, is_flag=True,
    help="List all snapshots for each volume, not just most recent")    
def list_snapshots(project, list_all):
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

                if s.state == 'completed' and not list_all: break
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
            if has_pending_snapshot(v):
                print("  Skipping {0}, snapshot already in progress".format(v.id))
                continue

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
            i.public_ip_address,
            i.private_ip_address,
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
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}. ".format(i.id) + str(e))
            continue

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
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}. ".format(i.id) + str(e))
            continue
    return

# as best practice to see if there's an imported function 
if __name__ == '__main__':
    cli()
