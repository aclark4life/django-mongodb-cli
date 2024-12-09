import click
import sys
import subprocess


@click.command()
def runserver(mongo_single, postgresql):
    """Start MongoDB and run the Django development server."""

    subprocess.run([sys.executable, "manage.py", "runserver"])
