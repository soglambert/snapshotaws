import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def cli():
    """shotty manages snapshots"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help='only instances for project (tag Project:<name>)')
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name
        )))
    return

@instances.command('stop')
@click.option('--project', default=None, help='only instances for project (tag Project:<name>)')

def stop_instances(project):
    "Stop EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--project', default=None, help='only instances for project (tag Project:<name>)')

def start_instances(project):
    "Start EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("Starting instances of {0}...".format(i.id))
        i.start()
    return

@volumes.command('list')
@click.option('--project', default=None, help='only volumes for project (tag Project:<name>)')
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
         print(i)
         for v in i.volumes.all():
             print(", ".join((
                 v.id,
                 i.id,
                 v.state,
                 str(v.size) + "Gib",
                 v.encrypted and "Encrypted" or "Not Encrypted"
             )))
    return


@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""
@snapshots.command('list')
@click.option('--project', default=None, help='only snapshots for project (tag Project:<name>)')
def list_volumes(project):
    "List EC2 volumes snapshots"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(",".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

@instances.command('snapshot', help="create snapshots")
@click.option('--project', default=None, help='only snapshots for project (tag Project:<name>)')
def create_snapshot(project):
    "Create volumes snapshots"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snaposhots of {0}...".format(v.id))
            v.create_snapshot(Description="by Leilei")
        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()
    print("Job's done!")    
    return


if __name__== '__main__':
    cli()
