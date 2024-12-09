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

    if not os.path.exists("manage.py"):
        click.echo("manage.py not found. Run `django-mongodb-cli startproject`!")
        return

    if make_migrations:
        subprocess.run([sys.executable, "manage.py", "makemigrations"])
    else:
        subprocess.run([sys.executable, "manage.py", "migrate"])
