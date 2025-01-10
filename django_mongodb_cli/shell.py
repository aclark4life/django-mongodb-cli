import click
import os
import sys
import subprocess


@click.command()
def shell():
    """Run management commands."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "shell"]
    else:
        command = ["django-admin", "shell"]  # Use a list for consistency

    subprocess.run(command)
