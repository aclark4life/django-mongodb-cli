import click
import subprocess


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def manage(args):
    """Run management commands."""
    subprocess.run(["python", "manage.py", *args])
