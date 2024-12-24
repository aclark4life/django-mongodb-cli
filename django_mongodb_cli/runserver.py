import click
import os
import sys
import subprocess


@click.command()
def runserver():
    """Start MongoDB and run the Django development server."""

    if os.environ.get("MONGODB_URI"):
        click.echo(os.environ["MONGODB_URI"])

    subprocess.run([sys.executable, "manage.py", "runserver"])
