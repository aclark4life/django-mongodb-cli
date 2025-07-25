import typer

from git import Repo

repo = typer.Typer()


@repo.command()
def status():
    repo = Repo(".")
    typer.echo(f"Active branch: {repo.active_branch}")
    for item in repo.index.diff(None):
        typer.echo(f"Modified: {item.a_path}")


# import os
# import subprocess
#
# import click
# from rich import print as rprint
# from black import format_str, Mode
#
# from .settings import test_settings_map
# from .utils import (
#    clone_repo,
#    copy_mongo_apps,
#    copy_mongo_migrations,
#    copy_mongo_settings,
#    get_management_command,
#    get_repos,
#    get_status,
#    get_repo_name_map,
#    install_package,
# )
#
#
# class Repo:
#    def __init__(self):
#        self.home = "src"
#
#    def __repr__(self):
#        return f"<Repo {self.home}>"
#
#
# pass_repo = click.make_pass_decorator(Repo)
#
#
# @click.group(invoke_without_command=True)
# @click.option(
#    "-l",
#    "--list-repos",
#    is_flag=True,
# )
# @click.pass_context
# def repo(context, list_repos):
#    context.obj = Repo()
#    repos, url_pattern, branch_pattern = get_repos("pyproject.toml")
#    if list_repos:
#        for repo_entry in repos:
#            click.echo(repo_entry)
#        return
#    if context.invoked_subcommand is None:
#        click.echo(context.get_help())
#
#
# @repo.command()
# @click.argument("repo_names", nargs=-1, required=False)
# @click.option(
#    "-a",
#    "--all-repos",
#    is_flag=True,
# )
# @click.option(
#    "-i",
#    "--install",
#    is_flag=True,
# )
# @click.pass_context
# @pass_repo
# def clone(repo, context, repo_names, all_repos, install):
#    repos, url_pattern, branch_pattern = get_repos("pyproject.toml")
#    repo_name_map = get_repo_name_map(repos, url_pattern)
#    if repo_names:
#        not_found = []
#        for name in repo_names:
#            repo_url = repo_name_map.get(name)
#            if repo_url:
#                clone_repo(repo_url, url_pattern, branch_pattern, repo)
#                if install:
#                    clone_path = os.path.join(context.obj.home, name)
#                    if os.path.exists(clone_path):
#                        install_package(clone_path)
#            else:
#                not_found.append(name)
#        if not_found:
#            for name in not_found:
#                click.echo(f"Repository '{name}' not found.")
#        return
#    if all_repos:
#        click.echo(f"Cloning {len(repos)} repositories...")
#        for name, repo_url in repo_name_map.items():
#            clone_repo(repo_url, url_pattern, branch_pattern, repo)
#            if install:
#                clone_path = os.path.join(context.obj.home, name)
#                if os.path.exists(clone_path):
#                    install_package(clone_path)
#        return
#
#    click.echo(context.get_help())
#
#
# @repo.command()
# @click.argument("repo_names", nargs=-1)
# @click.option("-a", "--all-repos", is_flag=True)
# @click.pass_context
# @pass_repo
# def install(repo, context, repo_names, all_repos):
#    repos, url_pattern, _ = get_repos("pyproject.toml")
#    repo_name_map = get_repo_name_map(repos, url_pattern)
#
#    if all_repos and repo_names:
#        click.echo("Cannot specify both repo names and --all-repos")
#        return
#
#    if all_repos:
#        click.echo(f"Updating {len(repo_name_map)} repositories...")
#        for repo_name, repo_url in repo_name_map.items():
#            clone_path = os.path.join(context.obj.home, repo_name)
#            if os.path.exists(clone_path):
#                install_package(clone_path)
#        return
#
#    if repo_names:
#        not_found = []
#        for repo_name in repo_names:
#            clone_path = os.path.join(context.obj.home, repo_name)
#            if os.path.exists(clone_path):
#                install_package(clone_path)
#            else:
#                not_found.append(repo_name)
#        for name in not_found:
#            click.echo(f"Repository '{name}' not found.")
#        return
#
#    click.echo(context.get_help())
#
#
# @repo.command(context_settings={"ignore_unknown_options": True})
# @click.argument("repo_name", required=False)
# @click.argument("args", nargs=-1)
# @click.pass_context
# def makemigrations(context, repo_name, args):
#    repos, url_pattern, _ = get_repos("pyproject.toml")
#
#    if repo_name:
#        repo_name_map = get_repo_name_map(repos, url_pattern)
#        if repo_name not in repo_name_map or repo_name not in test_settings_map:
#            click.echo(click.style(f"Repository '{repo_name}' not found.", fg="red"))
#            return
#        try:
#            copy_mongo_apps(repo_name)
#            copy_mongo_settings(
#                test_settings_map[repo_name]["settings"]["migrations"]["source"],
#                test_settings_map[repo_name]["settings"]["migrations"]["target"],
#            )
#        except FileNotFoundError:
#            click.echo(click.style(f"Settings for '{repo_name}' not found.", fg="red"))
#            return
#
#        command = get_management_command("makemigrations")
#        command.extend(
#            [
#                "--settings",
#                test_settings_map[repo_name]["settings"]["module"]["migrations"],
#            ]
#        )
#        if repo_name != "django-filter":
#            command.extend(
#                [
#                    "--pythonpath",
#                    os.path.join(os.getcwd(), test_settings_map[repo_name]["test_dir"]),
#                ]
#            )
#        if args:
#            command.extend(args)
#        click.echo(click.style(f"Running command: {' '.join(command)}", fg="blue"))
#        subprocess.run(command)
#        return
#
#    # No repo_name provided, show help
#    click.echo(context.get_help())
#
#
# @repo.command()
# @click.argument("repo_names", nargs=-1)
# @click.option("-a", "--all-repos", is_flag=True)
# @click.option("-r", "--reset", is_flag=True)
# @click.option("-d", "--diff", is_flag=True)
# @click.option("-b", "--branch", is_flag=True)
# @click.option("-u", "--update", is_flag=True)
# @click.option("-l", "--log", is_flag=True)
# @click.pass_context
# @pass_repo
# def status(repo, context, repo_names, all_repos, reset, diff, branch, update, log):
#    repos, url_pattern, _ = get_repos("pyproject.toml")
#    repo_name_map = get_repo_name_map(repos, url_pattern)
#
#    if repo_names:
#        not_found = []
#        for repo_name in repo_names:
#            repo_url = repo_name_map.get(repo_name)
#            if repo_url:
#                get_status(
#                    repo_url,
#                    url_pattern,
#                    repo,
#                    reset=reset,
#                    diff=diff,
#                    branch=branch,
#                    update=update,
#                    log=log,
#                )
#            else:
#                not_found.append(repo_name)
#        for name in not_found:
#            click.echo(f"Repository '{name}' not found.")
#        return
#
#    if all_repos:
#        click.echo(f"Status of {len(repos)} repositories...")
#        for repo_name, repo_url in repo_name_map.items():
#            get_status(
#                repo_url,
#                url_pattern,
#                repo,
#                reset=reset,
#                diff=diff,
#                branch=branch,
#                update=update,
#                log=log,
#            )
#        return
#
#    click.echo(context.get_help())
#
#
# @repo.command()
# @click.argument("repo_name", required=False)
# @click.argument("modules", nargs=-1)
# @click.option("-k", "--keyword")
# @click.option("-l", "--list-tests", is_flag=True)
# @click.option("-s", "--show-settings", is_flag=True)
# @click.option("-a", "--all-repos", is_flag=True)
# @click.option("--keepdb", is_flag=True)
# @click.pass_context
# def test(
#    context, repo_name, modules, keyword, list_tests, show_settings, keepdb, all_repos
# ):
#    repos, url_pattern, _ = get_repos("pyproject.toml")
#    repo_name_map = get_repo_name_map(repos, url_pattern)
#
#    if repo_name:
#        if repo_name not in repo_name_map or repo_name not in test_settings_map:
#            click.echo(
#                click.style(
#                    f"Repository/settings for '{repo_name}' not found.", fg="red"
#                )
#            )
#            return
#
#        if show_settings:
#            click.echo(f"⚙️  Test settings for 📦 {repo_name}:")
#            settings_dict = dict(sorted(test_settings_map[repo_name].items()))
#            formatted = format_str(str(settings_dict), mode=Mode())
#            rprint(formatted)
#            return
#
#        settings = test_settings_map[repo_name]
#        test_dirs = settings.get("test_dirs", [])
#
#        if list_tests:
#            for test_dir in test_dirs:
#                click.echo(f"📂 {test_dir}")
#                try:
#                    test_modules = sorted(os.listdir(test_dir))
#                    for module in test_modules:
#                        if module not in ("__pycache__", "__init__.py"):
#                            click.echo(click.style(f"    └── {module}", fg="green"))
#                    click.echo()
#                except FileNotFoundError:
#                    click.echo(
#                        click.style(f"Directory '{test_dir}' not found.", fg="red")
#                    )
#            return
#
#        if "settings" in settings:
#            repo_dir = os.path.join(context.obj.home, repo_name)
#            if not os.path.exists(repo_dir):
#                click.echo(
#                    click.style(
#                        f"Repository '{repo_name}' not found on disk.", fg="red"
#                    )
#                )
#                return
#            copy_mongo_settings(
#                settings["settings"]["test"]["source"],
#                settings["settings"]["test"]["target"],
#            )
#        else:
#            click.echo(click.style(f"Settings for '{repo_name}' not found.", fg="red"))
#            return
#
#        command = [settings["test_command"]]
#        copy_mongo_migrations(repo_name)
#        copy_mongo_apps(repo_name)
#
#        if (
#            settings["test_command"] == "./runtests.py"
#            and repo_name != "django-rest-framework"
#        ):
#            command.extend(
#                [
#                    "--settings",
#                    settings["settings"]["module"]["test"],
#                    "--parallel",
#                    "1",
#                    "--verbosity",
#                    "3",
#                    "--debug-sql",
#                    "--noinput",
#                ]
#            )
#        if keyword:
#            command.extend(["-k", keyword])
#        if keepdb:
#            command.append("--keepdb")
#
#        if repo_name in {
#            "django-debug-toolbar",
#            "django-allauth",
#            "django-mongodb-extensions",
#        }:
#            os.environ["DJANGO_SETTINGS_MODULE"] = settings["settings"]["module"][
#                "test"
#            ]
#            command.extend(
#                [
#                    "--continue-on-collection-errors",
#                    "--html=report.html",
#                    "--self-contained-html",
#                ]
#            )
#        elif repo_name == "mongo-python-driver":
#            command.extend(["test", "-s"])
#
#        command.extend(modules)
#        if os.environ.get("DJANGO_SETTINGS_MODULE"):
#            click.echo(
#                click.style(
#                    f"DJANGO_SETTINGS_MODULE={os.environ['DJANGO_SETTINGS_MODULE']}",
#                    fg="blue",
#                )
#            )
#        click.echo(click.style(f"Running {' '.join(command)}", fg="blue"))
#        subprocess.run(command, cwd=settings["test_dir"])
#        return
#
#    if all_repos and show_settings:
#        repos, url_pattern, _ = get_repos("pyproject.toml")
#        repo_name_map = get_repo_name_map(repos, url_pattern)
#        for repo_name in repo_name_map:
#            if repo_name in test_settings_map:
#                click.echo(f"⚙️  Test settings for 📦 {repo_name}:")
#                settings_dict = dict(sorted(test_settings_map[repo_name].items()))
#                formatted = format_str(str(settings_dict), mode=Mode())
#                rprint(formatted)
#            else:
#                click.echo(f"Settings for '{repo_name}' not found.")
#        return
#    else:
#        click.echo("Can only use --all-repos with --show-settings")
#        return
#
#    click.echo(context.get_help())
#
#
# @repo.command()
# @click.argument("repo_names", nargs=-1)
# @click.option("-a", "--all-repos", is_flag=True)
# @click.pass_context
# @pass_repo
# def update(repo, context, repo_names, all_repos):
#    repos, url_pattern, _ = get_repos("pyproject.toml")
#    repo_name_map = get_repo_name_map(repos, url_pattern)
#
#    if all_repos and repo_names:
#        click.echo("Cannot specify both repo names and --all-repos")
#        return
#
#    if all_repos:
#        click.echo(f"Updating {len(repo_name_map)} repositories...")
#        for repo_name, repo_url in repo_name_map.items():
#            get_status(
#                repo_url,
#                url_pattern,
#                repo,
#                update=True,  # Just like '-u' in status
#                reset=False,
#                diff=False,
#                branch=False,
#                log=False,
#            )
#        return
#
#    if repo_names:
#        not_found = []
#        for repo_name in repo_names:
#            repo_url = repo_name_map.get(repo_name)
#            if repo_url:
#                get_status(
#                    repo_url,
#                    url_pattern,
#                    repo,
#                    update=True,
#                    reset=False,
#                    diff=False,
#                    branch=False,
#                    log=False,
#                )
#            else:
#                not_found.append(repo_name)
#        for name in not_found:
#            click.echo(f"Repository '{name}' not found.")
#        return
#
#    click.echo(context.get_help())
