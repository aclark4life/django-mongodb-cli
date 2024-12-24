import click

from .createsuperuser import createsuperuser
from .install import install
from .manage import manage
from .migrate import migrate
from .repo import repo
from .runserver import runserver
from .test import test
from .startapp import startapp
from .startproject import startproject
from .startui import startui


@click.group()
def cli():
    pass


cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(manage)
cli.add_command(migrate)
cli.add_command(repo)
cli.add_command(runserver)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(startui)
cli.add_command(test)
