import click
import os
import sys
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def manage(args):
    """Run management commands."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py"]
    else:
        command = ["django-admin"]  # Use a list for consistency
    subprocess.run(command + [*args])
