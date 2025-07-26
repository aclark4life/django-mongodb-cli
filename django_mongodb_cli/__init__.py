import sys
import typer

from .app import app
from .project import project
from .repo import repo

dm = typer.Typer(
    help="\n\nDjango MongoDB CLI\n\nSystem executable:\n\n" + sys.executable
)


dm.add_typer(app, name="app")
dm.add_typer(project, name="project")
dm.add_typer(repo, name="repo")
