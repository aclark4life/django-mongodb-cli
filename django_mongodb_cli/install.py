import click


from .utils import get_management_command


@click.command()
def install():
    """Install development dependencies"""

    command = get_management_command()
    click.echo(f"Installing development dependencies using {command}...")
