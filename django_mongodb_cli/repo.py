import os
import subprocess

import click
from .config import test_settings_map
from .utils import (
    add_remote,
    apply_patches,
    clone_from,
    copy_mongo_apps,
    copy_mongo_migrations,
    copy_mongo_settings,
    get_management_command,
    get_repos,
    install_dependencies,
    pull,
)


class Repo:
    def __init__(self):
        self.home = "src"
        self.config = {}

    def set_config(self, key, value):
        self.config[key] = value

    def __repr__(self):
        return f"<Repo {self.home}>"


pass_repo = click.make_pass_decorator(Repo)


@click.group(invoke_without_command=True)
@click.option(
    "-l",
    "--list",
    is_flag=True,
    help="List all repositories in `pyproject.toml`.",
)
@click.pass_context
def repo(ctx, list):
    """
    Manage development repositories.
    """
    ctx.obj = Repo()
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if list:
        for repo_entry in repos:
            click.echo(repo_entry)
        return
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
)
@click.option(
    "-l",
    "--list",
    is_flag=True,
    help="List all branches/tracked files.",
)
@click.pass_context
@pass_repo
def clone(repo, ctx, src, all, list):
    """Clones a repository or repositories from `pyproject.toml`."""
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
                    clone_path = os.path.join(repo.home, repo_name)
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
                clone_path = os.path.join(repo.home, repo_name)
                clone_from(repo_url, clone_path, branch)
            else:
                click.echo(f"Invalid repository entry: {repo_entry}")
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command()
@click.pass_context
@pass_repo
def commit(repo, ctx):
    """
    Commit changes made in the specified repository.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
)
@click.argument("src", nargs=-1, type=click.Path())
@click.pass_context
@pass_repo
def install(repo, ctx, src, all):
    """`pip install` repository or repositories."""

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
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
)
@click.pass_context
@pass_repo
def fetch(repo, ctx, src, all):
    """Upstream"""
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        click.echo(f"Fetching {src}")
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name == src:
                    clone_path = os.path.join(repo.home, repo_name)
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
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all",
    is_flag=True,
)
@click.pass_context
@pass_repo
def update(repo, ctx, src, all):
    """Update"""
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name == src:
                    clone_path = os.path.join(repo.home, repo_name)
                    pull(clone_path)
    if all:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                clone_path = os.path.join("src", repo_name)
                pull(clone_path)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@repo.command(context_settings={"ignore_unknown_options": True})
@click.argument("src", required=False)
@click.argument("args", nargs=-1)
def makemigrations(
    src,
    args,
):
    """Run makemigrations."""

    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                if repo_name in test_settings_map.keys() and repo_name == src:
                    copy_mongo_apps(repo_name)
                    copy_mongo_settings(
                        test_settings_map[repo_name]["settings_file"]["migrate"]["src"],
                        test_settings_map[repo_name]["settings_file"]["migrate"][
                            "target"
                        ],
                    )
                    command = get_management_command("makemigrations")
                    command.extend(
                        [
                            "--settings",
                            test_settings_map[repo_name]["settings_module"]["migrate"],
                        ]
                    )
                    if not repo_name == "django-filter":
                        command.extend(
                            [
                                "--pythonpath",
                                os.path.join(
                                    os.getcwd(), test_settings_map[repo_name]["cwd"]
                                ),
                            ]
                        )
                    click.echo(f"Running command {' '.join(command)} {' '.join(args)}")
                    subprocess.run(command + [*args])


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
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
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
                            and repo_name != "drf-extensions"
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
