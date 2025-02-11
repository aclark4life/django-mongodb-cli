import click
import os
import subprocess


from .utils import get_management_command


@click.command()
def shell():
    """Run shell."""

    command = get_management_command()

    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mongo_settings"
    subprocess.run(command)
