import click
import sys
import subprocess


@click.command()
@click.option(
    "-mm", "--make-migrations", is_flag=True, help="Run Django makemigrations"
)
def migrate(mongo_single, postgresql, make_migrations):
    """Run Django migrations."""

    if make_migrations:
        subprocess.run([sys.executable, "manage.py", "makemigrations"])
    else:
        subprocess.run([sys.executable, "manage.py", "migrate"])
