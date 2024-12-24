import click
import os
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def manage(args):
    """Run management commands."""

    if os.path.exists("manage.py"):
        subprocess.run(["python", "manage.py", *args])
    else:
        subprocess.run(["django-admin", *args])
