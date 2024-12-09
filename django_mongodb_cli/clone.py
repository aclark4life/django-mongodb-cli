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
@click.option("-i", "--install", is_flag=True, help="Install checkouts")
@click.option("-l", "--list-checkouts", is_flag=True, help="List checkouts")
@click.option("-r", "--remote", is_flag=True, help="Add upstream remotes")
@click.option("-p", "--pre-commit", is_flag=True, help="Install pre-commit hooks")
@click.option("-u", "--update", is_flag=True, help="Update existing checkouts")
def clone(
    pyproject_path,
    clone_dir,
    delete,
    update,
    install,
    list_checkouts,
    remote,
    fetch,
    pre_commit,
):
    """Clone `dev` repositories in `tool.django_mongodb_cli` section of `pyproject.toml`."""
    if delete:
        if os.path.isdir("src"):
            shutil.rmtree("src")
            click.echo("Removed directory: src")
        else:
            click.echo("Skipping: src does not exist")
        exit()
    # Read and parse the pyproject.toml file
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)

    # Get the list of repositories
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])

    if not repos:
        click.echo("No repositories found under [tool.django_mongodb_cli] dev")
        return

    if list_checkouts:
        click.echo("\n".join(repos))
        exit()

    # Regex to extract the URL from the string
    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")
    branch_pattern = re.compile(
        r"git\+ssh://git@github\.com/[^/]+/[^@]+@([a-zA-Z0-9_\-\.]+)\b"
    )
    upstream_pattern = re.compile(r"#\s*upstream:\s*([\w-]+)")

    # Clone each repository
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

            if update:
                click.echo(f"Updating {repo_url} in {clone_path} (branch: {branch})")
                subprocess.run(["git", "pull"], cwd=clone_path)

            if install and os.path.exists(pyproject_toml):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", clone_path]
                )

            if install and os.path.exists(setup_py):
                subprocess.run([sys.executable, "setup.py", "develop"], cwd=clone_path)

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

            if remote and upstream_match:
                remote = f"https://github.com/{upstream_match.group(1)}/{repo_name}"
                subprocess.run(
                    ["git", "remote", "add", "upstream", remote], cwd=clone_path
                )
                subprocess.run(["git", "remote", "-v", "show"], cwd=clone_path)

            if fetch:
                subprocess.run(["git", "fetch", "upstream"], cwd=clone_path)

            if pre_commit:
                subprocess.run(["pre-commit", "install"], cwd=clone_path)
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")
    click.echo("All repositories cloned successfully.")
