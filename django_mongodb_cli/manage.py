import click

from django.core.management import execute_from_command_line


@click.command()
@click.argument("args", nargs=-1, required=False)
def manage(args, mongo_single, postgresql):
    """Run management commands."""

    execute_from_command_line(args)
