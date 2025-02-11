import click
import os
import sys
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def migrate(args):
    """Run migrate command."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "migrate"]
    else:
        command = ["django-admin", "migrate"]

    subprocess.run(command + [*args])
