import os
import subprocess

import click
from .config import test_settings_map
from .utils import (
    apply_patches,
    clone_repo,
    copy_mongo_apps,
    copy_mongo_migrations,
    copy_mongo_settings,
    fetch_repo,
    get_management_command,
    get_repos,
    install_repo,
    update_repo,
    status_repo,
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
    Manage development repositories for testing.
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
@click.argument("repo_names", nargs=-1, required=False)
@click.option(
    "-a",
    "--all-repos",
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
def clone(repo, ctx, repo_names, all_repos, list):
    """Clone repositories from `pyproject.toml`."""
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")

    if repo_names:
        for repo_name in repo_names:
            not_found = set()
            for repo_entry in repos:
                if (
                    os.path.basename(url_pattern.search(repo_entry).group(0))
                    == repo_name
                ):
                    clone_repo(repo_entry, url_pattern, branch_pattern, repo)
                    return
                else:
                    not_found.add(repo_name)
            click.echo(f"Repository '{not_found.pop()}' not found.")
        return

    if all_repos:
        click.echo(f"Cloning {len(repos)} repositories...")
        for repo_entry in repos:
            clone_repo(repo_entry, url_pattern, branch_pattern, repo)
        return

    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command()
@click.option(
    "-a",
    "--all-repos",
    is_flag=True,
)
@click.argument("repo_names", nargs=-1)
@click.pass_context
@pass_repo
def install(repo, ctx, repo_names, all_repos):
    """Install development repositories."""

    if repo_names:
        for repo_name in repo_names:
            clone_path = os.path.join("src", repo_name)
            if os.path.exists(clone_path):
                install_repo(clone_path)
            else:
                click.echo(f"Repository '{repo_name}' not found.")
        return

    if all_repos:
        repos, url_pattern, branch_pattern, upstream_pattern = get_repos(
            "pyproject.toml"
        )
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            if url_match:
                repo_url = url_match.group(0)
                repo_name = os.path.basename(repo_url)
                clone_path = os.path.join("src", repo_name)
                install_repo(clone_path)

    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all-repos",
    is_flag=True,
)
@click.pass_context
@pass_repo
def fetch(repo, ctx, src, all_repos):
    """Fetch upstream remotes for repositories."""
    repos, url_pattern, _, upstream_pattern = get_repos("pyproject.toml")
    if src:
        click.echo(f"Fetching upstream for {src}...")
        for repo_entry in repos:
            if os.path.basename(url_pattern.search(repo_entry).group(0)) == src:
                fetch_repo(repo_entry, upstream_pattern, url_pattern, repo)
                return  # Stop after finding the requested repo
        click.echo(f"Repository '{src}' not found.")
        return

    if all_repos:
        click.echo(f"Fetching upstream remotes for {len(repos)} repositories...")
        for repo_entry in repos:
            fetch_repo(repo_entry, upstream_pattern, url_pattern, repo)
        return

    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all-repos",
    is_flag=True,
)
@click.pass_context
@pass_repo
def update(repo, ctx, src, all_repos):
    """Update repositories."""
    repos, url_pattern, _, _ = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            if os.path.basename(url_pattern.search(repo_entry).group(0)) == src:
                update_repo(repo_entry, url_pattern, repo)
                return  # Stop after updating the requested repo
        click.echo(f"Repository '{src}' not found.")
        return

    if all_repos:
        click.echo(f"Updating {len(repos)} repositories...")
        for repo_entry in repos:
            update_repo(repo_entry, url_pattern, repo)
        return

    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command(context_settings={"ignore_unknown_options": True})
@click.argument("src", required=False)
@click.argument("args", nargs=-1)
@click.pass_context
def makemigrations(
    ctx,
    src,
    args,
):
    """Run makemigrations for test suites."""

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
    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("repo_name", required=False)
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-l", "--list-tests", help="List tests", is_flag=True)
@click.option("-s", "--setup", help="Setup tests", is_flag=True)
@click.pass_context
def test(
    ctx,
    repo_name,
    modules,
    keyword,
    list_tests,
    setup,
):
    """
    Run tests for Django and third-party libraries.
    """
    repos, url_pattern, branch_pattern, upstream_pattern = get_repos("pyproject.toml")
    if repo_name:
        for repo_entry in repos:
            url_match = url_pattern.search(repo_entry)
            repo_url = url_match.group(0)
            if repo_name == os.path.basename(repo_url):
                if repo_name in test_settings_map.keys():
                    test_dirs = test_settings_map[repo_name]["tests"]
                    if list_tests:
                        for test_dir in test_dirs:
                            click.echo(
                                click.style(f"Tests for '{test_dir}':", fg="blue")
                            )
                            try:
                                for module in sorted(os.listdir(test_dir)):
                                    click.echo(module)
                            except FileNotFoundError:
                                click.echo(
                                    click.style(
                                        f"Directory '{test_dir}' not found.", fg="red"
                                    )
                                )
                        return
                    if "settings_file" in test_settings_map[repo_name]:
                        copy_mongo_settings(
                            test_settings_map[repo_name]["settings_file"]["test"][
                                "src"
                            ],
                            test_settings_map[repo_name]["settings_file"]["test"][
                                "target"
                            ],
                        )
                    command = [test_settings_map[repo_name]["cmd"]]
                    apply_patches(repo_name)
                    copy_mongo_migrations(repo_name)
                    copy_mongo_apps(repo_name)
                    if (
                        repo_name != "django-rest-framework"
                        and repo_name != "django-allauth"
                        and repo_name != "django-debug-toolbar"
                        and repo_name != "mongo-python-driver"
                    ):
                        command.extend(
                            [
                                "--settings",
                                test_settings_map[repo_name]["settings_module"]["test"],
                                "--parallel",
                                "1",
                                "--verbosity",
                                "3",
                                "--debug-sql",
                                "--noinput",
                            ]
                        )
                    if keyword:
                        command.extend(["-k", keyword])
                    if (
                        repo_name == "django-debug-toolbar"
                        or repo_name == "django-allauth"
                    ):
                        os.environ["DJANGO_SETTINGS_MODULE"] = test_settings_map[
                            repo_name
                        ]["settings_module"]["test"]

                    if repo_name == "django-debug-toolbar":
                        command.extend(["-m", "django", "test"])

                    if repo_name == "mongo-python-driver" and setup:
                        command.extend(["setup-tests"])
                    elif repo_name == "mongo-python-driver":
                        command.extend(["run-tests"])

                    command.extend(modules)
                    click.echo(click.style(f"Running {' '.join(command)}", fg="blue"))
                    subprocess.run(command, cwd=test_settings_map[repo_name]["cwd"])
                else:
                    click.echo(f"Settings for '{repo_name}' not found.")
        return
    if ctx.args == []:
        click.echo(ctx.get_help())


@repo.command()
@click.argument("src", required=False)
@click.option(
    "-a",
    "--all-repos",
    is_flag=True,
)
@click.option(
    "-r",
    "--reset",
    is_flag=True,
)
@click.pass_context
@pass_repo
def status(repo, ctx, src, all_repos, reset):
    """Repository status."""
    repos, url_pattern, _, _ = get_repos("pyproject.toml")
    if src:
        for repo_entry in repos:
            if os.path.basename(url_pattern.search(repo_entry).group(0)) == src:
                status_repo(repo_entry, url_pattern, repo, reset=reset)
                return  # Stop after updating the requested repo
        click.echo(f"Repository '{src}' not found.")
        return

    if all_repos:
        click.echo(f"Status of {len(repos)} repositories...")
        for repo_entry in repos:
            status_repo(repo_entry, url_pattern, repo, reset=reset)
        return

    if ctx.args == []:
        click.echo(ctx.get_help())
