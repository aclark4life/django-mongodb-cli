import typer
import tempfile
import shutil
import subprocess
from pathlib import Path
import importlib.resources as resources

project = typer.Typer(help="Manage Django projects.")


@project.command("add")
def add_project(name: str, directory: Path = Path(".")):
    """
    Create a new Django project using bundled templates.
    """
    with resources.path(
        "django_mongodb_cli.templates", "project_template"
    ) as template_path:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            shutil.copytree(template_path, tmpdir / "project_template")

            cmd = [
                "django-admin",
                "startproject",
                "--template",
                str(tmpdir / "project_template"),
                name,
                str(directory),
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
