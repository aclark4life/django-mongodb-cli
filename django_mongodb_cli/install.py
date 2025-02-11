import click
import os
import subprocess
import sys


from .utils import get_management_command, get_repos


@click.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Install repos.",
)
def install(all):
    """Install development dependencies"""

    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")

    command = get_management_command()
    click.echo(f"Installing development dependencies using {' '.join(command)}...")

    if all:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                clone_path = os.path.join("src", repo_name)
                if os.path.exists("pyproject.toml"):
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-e", clone_path]
                    )
                if os.path.exists("setup.py"):
                    subprocess.run(
                        [sys.executable, "setup.py", "develop"], cwd=clone_path
                    )
