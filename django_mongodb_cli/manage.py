import click
import subprocess


@click.command()
def manage():
    """Run management commands."""
    subprocess.run(["python", "manage.py"])
