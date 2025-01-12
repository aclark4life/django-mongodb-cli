import click
import os
import sys
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def test(args):
    """Run test command."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "test"]
    else:
        command = ["django-admin", "test"]  # Use a list for consistency

    subprocess.run(command + [*args])
