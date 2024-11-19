import click
import git
import os
import re
import shutil
import sys
import subprocess
import toml


@click.command()
@click.argument(
    "pyproject_path", type=click.Path(exists=True), default="pyproject.toml"
)
@click.argument("clone_dir", type=click.Path(), default="src")
@click.option("-d", "--delete", is_flag=True, help="Delete existing checkouts")
def clone(pyproject_path, clone_dir, delete):
    """Clone repositories listed under [tool.django_mongodb_cli] dev in pyproject.toml."""
    if delete:
        if os.path.isdir("src"):
            shutil.rmtree("src")
            print("Removed directory: src")
        else:
            print("Skipping: src does not exist")
        exit()
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
    branch_pattern = re.compile(r"@([^@]+)$")

    # Clone each repository
    for repo_entry in repos:
        url_match = url_pattern.search(repo_entry)
        branch_match = branch_pattern.search(repo_entry)

        if url_match:
            repo_url = url_match.group(0)
            repo_name = os.path.basename(repo_url)
            branch = branch_match.group(1) if branch_match else "main"
            clone_path = os.path.join(clone_dir, repo_name)
            click.echo(f"Cloning {repo_url} into {clone_path} (branch: {branch})")
            try:
                git.Repo.clone_from(repo_url, clone_path, branch=branch)
            except git.exc.GitCommandError as e:
                click.echo(f"Failed to clone repository: {e}")
            pyproject_toml = os.path.join(clone_path, "pyproject.toml")
            if os.path.exists(pyproject_toml):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", clone_path]
                )
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")

    click.echo("All repositories cloned successfully.")


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startapp(delete):
    """Run startapp command with the template from src/django-mongodb-app."""
    if delete:
        if os.path.isdir("mongo_app"):
            shutil.rmtree("mongo_app")
            print("Removed directory: mongo_app")
        else:
            print("Skipping: mongo_app does not exist")
        exit()
    click.echo(
        subprocess.run(
            [
                sys.executable,
                "manage.py",
                "startapp",
                "mongo_app",
                "--template",
                os.path.join(os.path.join("src", "django-mongodb-app")),
            ]
        )
    )


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startproject(delete):
    """Run startproject command with the template from src/django-mongodb-project."""
    if delete:
        if os.path.isdir("mongo_project"):
            shutil.rmtree("mongo_project")
            print("Removed directory: mongo_project")
        else:
            print("Skipping: mongo_project does not exist")

        if os.path.isdir("mongo_migrations"):
            shutil.rmtree("mongo_migrations")
            print("Removed directory: mongo_migrations")
        else:
            print("Skipping: mongo_migrations does not exist")

        if os.path.isfile("manage.py"):
            os.remove("manage.py")
            print("Removed file: manage.py")
        else:
            print("Skipping: manage.py does not exist")

        exit()
    click.echo(
        subprocess.run(
            [
                "django-admin",
                "startproject",
                "mongo_project",
                ".",
                "--template",
                os.path.join(os.path.join("src", "django-mongodb-project")),
            ]
        )
    )


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
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(test)
