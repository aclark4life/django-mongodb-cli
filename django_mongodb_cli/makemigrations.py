import click
import os
import sys
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def makemigrations(args):
    """Run makemigrations."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "makemigrations"]
    else:
        command = ["django-admin", "makemigrations"]  # Use a list for consistency

    subprocess.run(command + [*args])
