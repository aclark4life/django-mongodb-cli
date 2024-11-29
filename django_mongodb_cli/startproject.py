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
        items = {
            "apps": os.path.isdir,
            "backend": os.path.isdir,
            "mongo_migrations": os.path.isdir,
            "manage.py": os.path.isfile,
        }

        for item, check_function in items.items():
            if check_function(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"Removed directory: {item}")
                elif os.path.isfile(item):
                    os.remove(item)
                    print(f"Removed file: {item}")
            else:
                print(f"Skipping: {item} does not exist")

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
