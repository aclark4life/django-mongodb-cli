import click
import sys
import subprocess

from .clone import clone
from .createsuperuser import createsuperuser
from .install import install
from .migrate import migrate
from .runtests import runtests
from .startapp import startapp
from .startproject import startproject
from .startui import startui
from .utils import mongo_launch, postgres_launch


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
@click.option(
    "-p",
    "--postgresql",
    is_flag=True,
    help="Launch a PostgreSQL instance",
)
def runserver(mongo_single, postgresql):
    """Start MongoDB and run the Django development server."""
    if mongo_single:
        mongodb = subprocess.Popen(mongo_launch())

    if postgresql:
        postgres = subprocess.Popen(postgres_launch())

    subprocess.run([sys.executable, "manage.py", "runserver"])

    if mongo_single:
        mongodb.terminate()

    if postgresql:
        postgres.terminate()


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(migrate)
cli.add_command(runserver)
cli.add_command(runtests)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(startui)
