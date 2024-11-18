import click
import os
import re
import shutil
import subprocess
import toml

from git import Repo


@click.command()
@click.argument(
    "pyproject_path", type=click.Path(exists=True), default="pyproject.toml"
)
@click.argument("clone_dir", type=click.Path(), default="src")
def clone(pyproject_path, clone_dir):
    """Clone repositories listed under [tool.django_mongodb_cli] dev in pyproject.toml."""
    # Read and parse the pyproject.toml file
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)

    # Get the list of repositories
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])

    if not repos:
        click.echo("No repositories found under [tool.django_mongodb_cli] dev")
        return

    # Regex to extract the URL from the string
    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")

    # Clone each repository
    for repo_entry in repos:
        match = url_pattern.search(repo_entry)
        if match:
            repo_url = match.group(0)
            repo_name = os.path.basename(repo_url)
            clone_path = os.path.join(clone_dir, repo_name)
            click.echo(f"Cloning {repo_url} into {clone_path}")
            Repo.clone_from(repo_url, clone_path)
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")

    click.echo("All repositories cloned successfully.")


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option(
    "-l", "--list-tests", default=False, is_flag=True, help="List available tests"
)
def test(modules, keyword, list_tests):
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
        "src/django-mongodb/.github/workflows/mongodb_settings.py",
        "src/django/tests/mongodb_settings.py",
    )

    command = ["src/django/tests/runtests.py"]
    command.extend(["--settings", "mongodb_settings"])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])

    # Add modules to the command
    command.extend(modules)

    # Add keyword filter if provided
    if keyword:
        command.extend(["-k", keyword])

    click.echo(f"Running command: {' '.join(command)}")

    # Start MongoDB
    mongodb = subprocess.Popen(["mongo-launch", "single"])

    # Execute the test command
    subprocess.run(command, stdin=None, stdout=None, stderr=None)

    # Terminate MongoDB
    mongodb.terminate()


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(test)
