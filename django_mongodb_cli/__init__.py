import click

from .createsuperuser import createsuperuser
from .manage import manage
from .migrate import migrate
from .repo import repo
from .runserver import runserver
from .shell import shell
from .startapp import startapp
from .startproject import startproject


@click.group()
def cli():
    pass


cli.add_command(createsuperuser)
cli.add_command(shell)
cli.add_command(manage)
cli.add_command(migrate)
cli.add_command(repo)
cli.add_command(runserver)
cli.add_command(startapp)
cli.add_command(startproject)
