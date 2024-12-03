import click
import sys
import subprocess

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
