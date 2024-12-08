import click
import git
import os
import re
import shutil
import sys
import subprocess
import toml


@click.command()
@click.argument(
    "pyproject_path", type=click.Path(exists=True), default="pyproject.toml"
)
@click.argument("clone_dir", type=click.Path(), default="src")
@click.option("-d", "--delete", is_flag=True, help="Delete existing checkouts")
@click.option("-f", "--fetch", is_flag=True, help="Fetch from remotes")
@click.option("-r", "--remote", is_flag=True, help="Add upstream remotes")
@click.option("-u", "--update", is_flag=True, help="Update existing checkouts")
def clone(
    pyproject_path,
    clone_dir,
    delete,
    update,
    remote,
    fetch,
):
    """Clone repositories listed in pyproject.toml."""

    # Delete existing checkouts
    if delete:
        if os.path.isdir("src"):
            shutil.rmtree("src")
            click.echo("Removed directory: src")
        else:
            click.echo("Skipping: src does not exist")
        return

    # Get repositories from pyproject.toml
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])
    if not repos:
        click.echo("No repositories found under [tool.django_mongodb_cli] dev")
        return

    # Regular expressions to extract repository URL, branch, and upstream
    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")
    branch_pattern = re.compile(
        r"git\+ssh://git@github\.com/[^/]+/[^@]+@([a-zA-Z0-9_\-\.]+)\b"
    )
    upstream_pattern = re.compile(r"#\s*upstream:\s*([\w-]+)")

    # Clone repositories
    for repo_entry in repos:
        url_match = url_pattern.search(repo_entry)
        branch_match = branch_pattern.search(repo_entry)
        upstream_match = upstream_pattern.search(repo_entry)
        if url_match:
            repo_url = url_match.group(0)
            repo_name = os.path.basename(repo_url)
            branch = branch_match.group(1) if branch_match else "main"
            clone_path = os.path.join(clone_dir, repo_name)
            pyproject_toml = os.path.join(clone_path, "pyproject.toml")
            setup_py = os.path.join(clone_path, "setup.py")

            # Clone repository
            if not os.path.exists(clone_path):
                click.echo(f"Cloning {repo_url} into {clone_path} (branch: {branch})")
                try:
                    git.Repo.clone_from(repo_url, clone_path, branch=branch)
                except git.exc.GitCommandError:
                    try:
                        git.Repo.clone_from(repo_url, clone_path)
                    except git.exc.GitCommandError as e:
                        click.echo(f"Failed to clone repository: {e}")
            else:
                click.echo(f"Skipping {repo_url} in {clone_path} (branch: {branch})")

            # Install package in development mode
            if os.path.exists(pyproject_toml):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", clone_path]
                )
            if os.path.exists(setup_py):
                subprocess.run([sys.executable, "setup.py", "develop"], cwd=clone_path)

            # Install pre-commit hooks
            if os.path.isfile(os.path.join(clone_path, ".pre-commit-config.yaml")):
                subprocess.run(["pre-commit", "install"], cwd=clone_path)

            # Conditionally fetch from remotes, update checkouts, and add upstream remotes
            if fetch:
                subprocess.run(["git", "fetch", "upstream"], cwd=clone_path)
            if update:
                click.echo(f"Updating {repo_url} in {clone_path} (branch: {branch})")
                subprocess.run(["git", "pull"], cwd=clone_path)
            if remote and upstream_match:
                remote = f"https://github.com/{upstream_match.group(1)}/{repo_name}"
                subprocess.run(
                    ["git", "remote", "add", "upstream", remote], cwd=clone_path
                )
                subprocess.run(["git", "remote", "-v", "show"], cwd=clone_path)
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")
    click.echo("All repositories cloned successfully.")
