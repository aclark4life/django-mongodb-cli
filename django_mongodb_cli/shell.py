import click
import os
import sys
import subprocess


@click.command()
def shell():
    """Run shell."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "shell"]
    else:
        command = ["django-admin", "shell"]  # Use a list for consistency

    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mongo_settings"
    subprocess.run(command)
