import click
import os
import sys
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("-w", "--wagtail", is_flag=True, help="Run makemigrations for Wagtail.")
@click.argument("args", nargs=-1)
def makemigrations(args, wagtail):
    """Run makemigrations."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "makemigrations"]
    else:
        command = ["django-admin", "makemigrations"]  # Use a list for consistency

    if wagtail:
        os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail.test.settings"

    subprocess.run(command + [*args])
