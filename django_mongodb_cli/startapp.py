import click
import os
import sys
import subprocess


@click.command()
@click.argument("name")
def startapp(name):
    """Run startapp command with the template from src/django-mongodb-app."""
    if os.path.exists("manage.py"):
        click.echo(
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "startapp",
                    name,
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )
    else:
        click.echo(
            subprocess.run(
                [
                    "django-admin",
                    "startapp",
                    name,
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )
