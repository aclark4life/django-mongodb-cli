import click
import os
import shutil
import subprocess


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
def runtests(modules, keyword, show_tests, show_command):
    """
    Run tests for specified modules with an optional keyword filter.
    """

    if not os.path.isdir(os.path.join("src", "django")):
        click.echo("Please run `django-mongodb-cli clone` first!")
        return

    shutil.copyfile(
        "mongodb_settings.py",
        os.path.join("src", "django", "tests", "mongodb_settings.py"),
    )

    command = ["src/django/tests/runtests.py"]
    command.extend(["--settings", "mongodb_settings"])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])
    command.extend(["--noinput"])
    command.extend(modules)

    if keyword:
        command.extend(["-k", keyword])

    subprocess.run(command, stdin=None, stdout=None, stderr=None)
