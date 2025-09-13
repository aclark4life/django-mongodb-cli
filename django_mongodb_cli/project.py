import typer
import shutil
from pathlib import Path
import subprocess
import importlib.resources as resources

project = typer.Typer(help="Manage Django projects.")


@project.command("add")
def add_project(name: str, directory: Path = Path(".")):
    """
    Create a new Django project using bundled templates.
    """
    # Get the real path to the embedded project_template folder
    with resources.path(
        "django_mongodb_cli.templates", "project_template"
    ) as template_path:
        cmd = [
            "django-admin",
            "startproject",
            "--template",
            str(template_path),
            name,
            # str(directory),
        ]
        typer.echo(f"Creating project: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)


@project.command("remove")
def remove_project(name: str, directory: Path = Path(".")):
    """
    Delete a Django project by name.
    """
    target = directory / name
    if target.exists() and target.is_dir():
        shutil.rmtree(target)
        typer.echo(f"Removed project {name}")
    else:
        typer.echo(f"Project {name} does not exist.", err=True)
