import click
import subprocess

from .utils import get_management_command


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def test(args):
    """Run test command."""

    command = get_management_command()

    subprocess.run(command + [*args])
