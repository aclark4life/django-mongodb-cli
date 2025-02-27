import os
import subprocess

import click
from .config import test_settings_map
from .utils import (
    get_repos,
    clone_from,
    add_remote,
    pull,
    install_dependencies,
    apply_patches,
    copy_mongo_apps,
    copy_mongo_migrations,
    copy_mongo_settings,
)


class Repo:
    def __init__(self, home):
        self.home = home
        self.config = {}

    def set_config(self, key, value):
        self.config[key] = value

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
@click.version_option("1.0")
@click.pass_context
def repo(ctx, repo_home, config):
    """Repo is a command line tool that showcases how to build complex
    command line interfaces with Click.

    This tool is supposed to look like a distributed version control
    system to show how something like this can be structured.
    """
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_repo decorator.
    ctx.obj = Repo(os.path.abspath(repo_home))
    for key, value in config:
        ctx.obj.set_config(key, value)


@repo.command()
@click.argument("src", required=False)
@click.argument("dest", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Check out all branches/tracked files.",
)
@click.option(
    "-l",
    "--list",
    is_flag=True,
    help="List all branches/tracked files.",
)
@pass_repo
def clone(repo, src, dest, all, list):
    """Clones a repository.

    This will clone the repository at SRC into the folder DEST.  If DEST
    is not provided this will automatically use the last path component
    of SRC and create that folder.
    """
    if dest is None:
        dest = "src"
    repo.home = dest
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")

    if list:
        for repo_entry in repos:
            click.echo(repo_entry)
        return
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
                    if not os.path.exists(clone_path):
                        clone_from(repo_url, clone_path, branch)
                    else:
                        click.echo(f"Repository {repo_name} already exists.")
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
        install_dependencies(clone_path)

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
                install_dependencies(clone_path)


@repo.command()
@click.argument("src", required=False)
@click.argument("dest", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Check out all branches/tracked files.",
)
@pass_repo
def fetch(repo, src, dest, all):
    """Upstream"""
    if dest is None:
        dest = "src"
    repo.home = dest
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        click.echo(f"Fetching {src}")
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name == src:
                    clone_path = os.path.join(dest, repo_name)
                    upstream_match = upstream_pattern.search(repo_entry)
                    if upstream_match:
                        add_remote(upstream_match, clone_path, repo_name)
    if all:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                clone_path = os.path.join("src", repo_name)
                upstream_match = upstream_pattern.search(repo_entry)
                if upstream_match:
                    add_remote(upstream_match, clone_path, repo_name)


@repo.command()
@click.argument("src", required=False)
@click.argument("dest", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Check out all branches/tracked files.",
)
@pass_repo
def update(repo, src, dest, all):
    """Update"""
    if dest is None:
        dest = "src"
    repo.home = dest
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name == src:
                    clone_path = os.path.join(dest, repo_name)
                    pull(clone_path)
    if all:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                clone_path = os.path.join("src", repo_name)
                pull(clone_path)


@repo.command()
@click.argument("src", required=False)
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-l", "--list-tests", help="List tests", is_flag=True)
def test(
    src,
    modules,
    keyword,
    list_tests,
):
    """
    Run `runtests.py` for Django or Wagtail.
    """
    dest = "src"
    repo.home = dest
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            # branch_match = branch_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name in test_settings_map.keys():
                    test_dirs = test_settings_map[repo_name]["test_dirs"]
                    if repo_name == src:
                        if list_tests:
                            for test_dir in test_dirs:
                                for module in sorted(os.listdir(test_dir)):
                                    click.echo(module)
                            return
                        copy_mongo_settings(
                            test_settings_map[repo_name]["settings_file"]["test"][
                                "src"
                            ],
                            test_settings_map[repo_name]["settings_file"]["test"][
                                "target"
                            ],
                        )
                        command = [test_settings_map[repo_name]["command"]]
                        apply_patches(repo_name)
                        copy_mongo_migrations(repo_name)
                        copy_mongo_apps(repo_name)
                        if (
                            repo_name != "django-rest-framework"
                            and repo_name != "django-allauth"
                            and repo_name != "django-debug-toolbar"
                        ):
                            command.extend(
                                [
                                    "--settings",
                                    test_settings_map[repo_name]["settings_module"][
                                        "test"
                                    ],
                                    "--parallel",
                                    "1",
                                    "--verbosity",
                                    "3",
                                    "--debug-sql",
                                    "--noinput",
                                ]
                            )
                        command.extend(modules)
                        if keyword:
                            command.extend(["-k", keyword])
                        click.echo(
                            click.style(f"Running {' '.join(command)}", fg="blue")
                        )
                        if repo_name == "django-debug-toolbar":
                            # For pytest to use correct settings file.
                            os.environ["DJANGO_SETTINGS_MODULE"] = test_settings_map[
                                repo_name
                            ]["settings_module"]["tests"]
                        subprocess.run(command, cwd=test_settings_map[repo_name]["cwd"])
