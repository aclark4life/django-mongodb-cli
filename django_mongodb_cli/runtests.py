import click
import os
import shutil
import subprocess


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option(
    "-l", "--list-tests", default=False, is_flag=True, help="List available tests"
)
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
@click.option(
    "--dry-run", is_flag=True, help="Perform a dry run without executing tests"
)
def runtests(modules, keyword, list_tests, dry_run, mongo_single):
    """
    Run tests for specified modules with an optional keyword filter.
    """
    if list_tests:
        click.echo(subprocess.run(["ls", os.path.join("src", "django", "tests")]))
        click.echo(
            subprocess.run(["ls", os.path.join("src", "django-mongodb", "tests")])
        )
        exit()

    shutil.copyfile(
        "mongodb_settings.py",
        "src/django/tests/mongodb_settings.py",
    )

    command = ["src/django/tests/runtests.py"]
    command.extend(["--settings", "mongodb_settings"])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])
    command.extend(["--noinput"])

    # Add modules to the command
    command.extend(modules)

    # Add keyword filter if provided
    if keyword:
        command.extend(["-k", keyword])

    click.echo(f"Running command: {' '.join(command)}")
    if dry_run:
        exit()

    if mongo_single:
        # Start MongoDB
        mongodb = subprocess.Popen(["mongo-launch", "single"])

    # Execute the test command
    subprocess.run(command, stdin=None, stdout=None, stderr=None)

    if mongo_single:
        # Terminate MongoDB
        mongodb.terminate()
