import click
import sys
import subprocess

from .utils import mongo_launch, postgres_launch


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
@click.option(
    "-p",
    "--postgresql",
    is_flag=True,
    help="Launch a PostgreSQL instance",
)
@click.option(
    "-mm", "--make-migrations", is_flag=True, help="Run Django makemigrations"
)
def migrate(mongo_single, postgresql, make_migrations):
    """Run Django migrations."""
    if mongo_single:
        mongodb = subprocess.Popen(mongo_launch())

    if postgresql:
        postgres = subprocess.Popen(postgres_launch())

    if make_migrations:
        subprocess.run([sys.executable, "manage.py", "makemigrations"])
    else:
        subprocess.run([sys.executable, "manage.py", "migrate"])

    if mongo_single:
        mongodb.terminate()

    if postgresql:
        postgres.terminate()
