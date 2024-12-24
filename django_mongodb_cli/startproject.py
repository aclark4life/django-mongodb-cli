import click
import os
import shutil
import subprocess


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
@click.option("-dj", "--django", is_flag=True, help="Use django mongodb template")
@click.option("-w", "--wagtail", is_flag=True, help="Use wagtail mongodb template")
@click.argument("project_name", required=False, default="backend")
def startproject(
    delete,
    django,
    wagtail,
    project_name,
):
    """Run startproject command with the template from src/django-mongodb-project."""

    click.echo(project_name)

    if os.path.exists("manage.py"):
        click.echo("manage.py already exists")
        if not delete:
            click.echo("Use -d to delete existing project files")
            return

    if delete:
        items = {
            ".dockerignore": os.path.isfile,
            "Dockerfile": os.path.isfile,
            "apps": os.path.isdir,
            "home": os.path.isdir,
            "backend": os.path.isdir,
            "db.sqlite3": os.path.isfile,
            "mongo_migrations": os.path.isdir,
            "manage.py": os.path.isfile,
            "requirements.txt": os.path.isfile,
            "search": os.path.isdir,
        }

        for item, check_function in items.items():
            if check_function(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    click.echo(f"Removed directory: {item}")
                elif os.path.isfile(item):
                    os.remove(item)
                    click.echo(f"Removed file: {item}")
            else:
                click.echo(f"Skipping: {item} does not exist")

        return

    template = None
    django_admin = "django-admin"
    startproject = "startproject"
    if wagtail:
        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
        django_admin = "wagtail"
        startproject = "start"
    elif django:
        template = os.path.join(os.path.join("src", "django-mongodb-project"))

    if not template:
        template = os.path.join(os.path.join("project_template"))

    click.echo(
        subprocess.run(
            [
                django_admin,
                startproject,
                project_name,
                ".",
                "--template",
                template,
            ]
        )
    )
