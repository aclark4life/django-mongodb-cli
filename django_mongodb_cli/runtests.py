import click
import os
import shutil
import subprocess


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option(
    "-l", "--show-tests", default=False, is_flag=True, help="List available tests"
)
@click.option(
    "-d",
    "--show-command",
    is_flag=True,
    help="Perform a dry run without executing tests",
)
def runtests(modules, keyword, show_tests, show_command):
    """
    Run tests for specified modules with an optional keyword filter.
    """

    if not os.path.isdir(os.path.join("src", "django")):
        click.echo("Please run `django-mongodb-cli clone` first!")
        exit()

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

    if show_command:
        click.echo(f"Running command: {' '.join(command)}")
        exit()

    if show_tests:
        click.echo(subprocess.run(["ls", os.path.join("src", "django", "tests")]))
        click.echo(
            subprocess.run(["ls", os.path.join("src", "django-mongodb", "tests")])
        )
        exit()

    if os.environ.get("DATABASE_URL"):
        subprocess.run(command, stdin=None, stdout=None, stderr=None)
    else:
        click.echo("Please set the DATABASE_URL environment variable!")
