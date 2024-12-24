import click
import os
import sys
import subprocess


@click.command()
@click.option(
    "-mm", "--make-migrations", is_flag=True, help="Run Django makemigrations"
)
def migrate(make_migrations):
    """Run Django migrations."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py"]
    else:
        command = ["django-admin"]  # Use a list for consistency

    if os.environ.get("MONGODB_URI"):
        click.echo(os.environ["MONGODB_URI"])

    if make_migrations:
        subprocess.run(command + ["makemigrations"])
    else:
        subprocess.run(command + ["migrate"])
