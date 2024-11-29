import click
import os
import shutil
import sys
import subprocess

from .clone import clone
from .createsuperuser import createsuperuser
from .install import install


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
def migrate(mongo_single):
    """Run Django migrations."""
    if mongo_single:
        mongodb = subprocess.Popen(["mongo-launch", "single"])
    subprocess.run([sys.executable, "manage.py", "migrate"])
    if mongo_single:
        mongodb.terminate()


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
def runserver(mongo_single):
    """Start MongoDB and run the Django development server."""
    if mongo_single:
        mongodb = subprocess.Popen(["mongo-launch", "single"])
    subprocess.run([sys.executable, "manage.py", "runserver"])
    if mongo_single:
        mongodb.terminate()


@click.command()
@click.argument("name")
def startapp(name):
    """Run startapp command with the template from src/django-mongodb-app."""
    if os.path.exists("manage.py"):
        click.echo(
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "startapp",
                    name,
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )
    else:
        click.echo(
            subprocess.run(
                [
                    "django-admin",
                    "startapp",
                    name,
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
@click.option("-w", "--wagtail-project", is_flag=True, help="Use wagtail template")
def startproject(delete, wagtail_project):
    """Run startproject command with the template from src/django-mongodb-project."""
    if delete:
        if os.path.isdir("backend"):
            shutil.rmtree("backend")
            print("Removed directory: backend")
        else:
            print("Skipping: backend does not exist")

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

    if wagtail_project:
        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
    else:
        template = os.path.join(os.path.join("src", "django-mongodb-project"))

    click.echo(
        subprocess.run(
            [
                "django-admin",
                "startproject",
                "backend",
                ".",
                "--template",
                template,
            ]
        )
    )


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startui(delete):
    """Run webpack_init command to create frontend directory."""
    if delete:
        if os.path.isdir("frontend"):
            shutil.rmtree("frontend")
            print("Removed directory: frontend")
        else:
            print("Skipping: frontend does not exist")

        for frontend_file in [
            ".babelrc",
            ".browserslistrc",
            ".eslintrc",
            ".nvmrc",
            ".stylelintrc.json",
            "package-lock.json",
            "package.json",
            "postcss.config.js",
        ]:
            if os.path.isfile(frontend_file):
                os.remove(frontend_file)
                print(f"Removed file: {frontend_file}")
            else:
                print(f"Skipping: {frontend_file} does not exist")
        exit()

    click.echo(
        subprocess.run([sys.executable, "manage.py", "webpack_init", "--no-input"])
    )


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
def test(modules, keyword, list_tests, dry_run, mongo_single):
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


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(migrate)
cli.add_command(runserver)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(startui)
cli.add_command(test)
