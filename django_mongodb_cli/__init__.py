import click
import os
import shutil
import sys
import subprocess

from .clone import clone
from .createsuperuser import createsuperuser
from .install import install
from .runtests import runtests
from .startapp import startapp


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
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
@click.option("-wm", "--wagtail-mongodb", is_flag=True, help="Use wagtail template")
@click.option("-dm", "--django-mongodb", is_flag=True, help="Use wagtail template")
def startproject(delete, wagtail_mongodb, django_mongodb):
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

    if wagtail_mongodb:
        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
    elif django_mongodb:
        template = os.path.join(os.path.join("src", "django-mongodb-project"))

    if wagtail_mongodb or django_mongodb:
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
    else:
        click.echo(
            subprocess.run(
                [
                    "django-admin",
                    "startproject",
                    "backend",
                    ".",
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


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(migrate)
cli.add_command(runserver)
cli.add_command(runtests)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(startui)
