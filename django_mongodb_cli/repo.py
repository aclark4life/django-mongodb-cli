import os
import sys
import subprocess

import click
from .utils import get_repos, clone_from


class Repo:
    def __init__(self, home):
        self.home = home
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo(f"  config[{key}] = {value}", file=sys.stderr)

    def __repr__(self):
        return f"<Repo {self.home}>"


pass_repo = click.make_pass_decorator(Repo)


@click.group()
@click.option(
    "--repo-home",
    envvar="REPO_HOME",
    default=".repo",
    metavar="PATH",
    help="Changes the repository folder location.",
)
@click.option(
    "--config",
    nargs=2,
    multiple=True,
    metavar="KEY VALUE",
    help="Overrides a config key/value pair.",
)
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.version_option("1.0")
@click.pass_context
def repo(ctx, repo_home, config, verbose):
    """Repo is a command line tool that showcases how to build complex
    command line interfaces with Click.

    This tool is supposed to look like a distributed version control
    system to show how something like this can be structured.
    """
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_repo decorator.
    ctx.obj = Repo(os.path.abspath(repo_home))
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)


@repo.command()
@click.argument("src", required=False)
@click.argument("dest", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Check out all branches/tracked files instead.",
)
@pass_repo
def clone(repo, src, dest, all):
    """Clones a repository.

    This will clone the repository at SRC into the folder DEST.  If DEST
    is not provided this will automatically use the last path component
    of SRC and create that folder.
    """
    if dest is None:
        dest = "src"
    repo.home = dest
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            branch_match = branch_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name == src:
                    branch = branch_match.group(1) if branch_match else "main"
                    clone_path = os.path.join(dest, repo_name)
                    clone_from(repo_url, clone_path, branch)
    if all:
        click.echo(f"Checking out {len(repos)} repositories")
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            branch_match = branch_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                branch = branch_match.group(1) if branch_match else "main"
                clone_path = os.path.join(dest, repo_name)
                clone_from(repo_url, clone_path, branch)
            else:
                click.echo(f"Invalid repository entry: {repo_entry}")


@repo.command()
@click.confirmation_option()
@pass_repo
def delete(repo):
    """Deletes a repository.

    This will throw away the current repository.
    """
    click.echo(f"Destroying repo {repo.home}")
    click.echo("Deleted!")


@repo.command()
@click.option("--username", prompt=True, help="The developer's shown username.")
@click.option("--email", prompt="E-Mail", help="The developer's email address")
@click.password_option(help="The login password.")
@pass_repo
def setuser(repo, username, email, password):
    """Sets the user credentials.

    This will override the current user config.
    """
    repo.set_config("username", username)
    repo.set_config("email", email)
    repo.set_config("password", "*" * len(password))
    click.echo("Changed credentials.")


@repo.command()
@click.option(
    "--message",
    "-m",
    multiple=True,
    help="The commit message.  If provided multiple times each"
    " argument gets converted into a new line.",
)
@click.argument("files", nargs=-1, type=click.Path())
@pass_repo
def commit(repo, files, message):
    """Commits outstanding changes.

    Commit changes to the given files into the repository.  You will need to
    "repo push" to push up your changes to other repositories.

    If a list of files is omitted, all changes reported by "repo status"
    will be committed.
    """
    if not message:
        marker = "# Files to be committed:"
        hint = ["", "", marker, "#"]
        for file in files:
            hint.append(f"#   U {file}")
        message = click.edit("\n".join(hint))
        if message is None:
            click.echo("Aborted!")
            return
        msg = message.split(marker)[0].rstrip()
        if not msg:
            click.echo("Aborted! Empty commit message")
            return
    else:
        msg = "\n".join(message)
    click.echo(f"Files to be committed: {files}")
    click.echo(f"Commit message:\n{msg}")


@repo.command(short_help="Copies files.")
@click.option(
    "--force", is_flag=True, help="forcibly copy over an existing managed file"
)
@click.argument("src", nargs=-1, type=click.Path())
@click.argument("dst", type=click.Path())
@pass_repo
def copy(repo, src, dst, force):
    """Copies one or multiple files to a new location.  This copies all
    files from SRC to DST.
    """
    for fn in src:
        click.echo(f"Copy from {fn} -> {dst}")


@repo.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Install repos.",
)
@click.argument("src", nargs=-1, type=click.Path())
@pass_repo
def install(repo, src, all):
    """Install development dependencies"""

    if src:
        clone_path = os.path.join("src", src[0])
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", clone_path])

    if all:
        repos, url_pattern, branch_pattern, upstream_pattern = get_repos(
            "pyproject.toml"
        )
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
