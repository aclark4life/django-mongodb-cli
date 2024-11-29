import click
import os
import shutil
import subprocess


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
