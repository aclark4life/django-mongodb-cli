import click
import os
import shutil
import subprocess


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
@click.option(
    "-wm", "--wagtail-mongodb", is_flag=True, help="Use wagtail mongodb template"
)
@click.option(
    "-wp", "--wagtail-postgres", is_flag=True, help="Use wagtail postgres template"
)
@click.option(
    "-dm", "--django-mongodb", is_flag=True, help="Use django mongodb template"
)
@click.option(
    "-dp", "--django-postgres", is_flag=True, help="Use django postgres template"
)
def startproject(
    delete, wagtail_mongodb, wagtail_postgres, django_mongodb, django_postgres
):
    """Run startproject command with the template from src/django-mongodb-project."""

    if delete:
        items = {
            "backend": os.path.isdir,
            "db.sqlite3": os.path.isfile,
            "home": os.path.isdir,
            "mongo_migrations": os.path.isdir,
            "manage.py": os.path.isfile,
            "search": os.path.isdir,
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

    template = None
    if wagtail_mongodb:
        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
    elif wagtail_postgres:
        template = os.path.join(os.path.join("src", "wagtail-postgresql-project"))
    elif django_mongodb:
        template = os.path.join(os.path.join("src", "django-mongodb-project"))
    elif django_postgres:
        template = os.path.join(os.path.join("src", "django-postgresql-project"))

    if template:
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