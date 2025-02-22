import click
import subprocess

from .utils import get_management_command


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def migrate(args):
    """Run migrate command."""

    command = get_management_command("migrate")
    subprocess.run(command + [*args])
