import click
import subprocess

from django.core.management import execute_from_command_line
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
@click.argument("args", nargs=-1, required=False)
def manage(args, mongo_single, postgresql):
    """Run management commands."""
    if mongo_single:
        mongodb = subprocess.Popen(mongo_launch())

    if postgresql:
        postgres = subprocess.Popen(postgres_launch())

    execute_from_command_line(args)

    if mongo_single:
        mongodb.terminate()

    if postgresql:
        postgres.terminate()
