import click

from .clone import clone
from .createsuperuser import createsuperuser
from .install import install

from .migrate import migrate
from .runserver import runserver
from .runtests import runtests
from .startapp import startapp
from .startproject import startproject
from .startui import startui


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(migrate)
cli.add_command(runserver)
cli.add_command(runtests)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(startui)
