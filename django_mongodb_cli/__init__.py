import sys
import typer

from .repo import repo

dm = typer.Typer(
    help="\n\nDjango MongoDB CLI\n\nSystem executable:\n\n" + sys.executable,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


dm.add_typer(repo, name="repo")
