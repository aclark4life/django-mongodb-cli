import click
import os
import subprocess


from .config import test_settings_map


from .utils import (
    apply_patches,
    copy_mongo_apps,
    copy_mongo_migrations,
    copy_mongo_settings,
    get_repo_name,
)


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-a", "--django-allauth", help="Run Django Allauth tests", is_flag=True)
@click.option(
    "-d", "--django-debug-toolbar", help="Run Django Debug Toolbar tests", is_flag=True
)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-f", "--django-filter", help="Run Django Filter tests", is_flag=True)
@click.option(
    "-r",
    "--django-rest-framework",
    help="Run Django Rest Framework tests",
    is_flag=True,
)
@click.option("-l", "--list-tests", help="List tests", is_flag=True)
@click.option("-w", "--wagtail", help="Run Wagtail tests", is_flag=True)
def runtests(
    modules,
    keyword,
    list_tests,
    wagtail,
    django_filter,
    django_rest_framework,
    django_allauth,
    django_debug_toolbar,
):
    """
    Run `runtests.py` for Django or Wagtail.
    """
    repo_name = get_repo_name(
        django_allauth,
        django_debug_toolbar,
        django_filter,
        django_rest_framework,
        wagtail,
    )
    test_dirs = test_settings_map[repo_name]["test_dirs"]
    if list_tests:
        for test_dir in test_dirs:
            for module in sorted(os.listdir(test_dir)):
                click.echo(module)
        return
    copy_mongo_settings(
        test_settings_map[repo_name]["settings_file"]["test"]["src"],
        test_settings_map[repo_name]["settings_file"]["test"]["target"],
    )
    command = [test_settings_map[repo_name]["command"]]
    apply_patches(repo_name)
    copy_mongo_migrations(repo_name)
    copy_mongo_apps(repo_name)
    if (
        repo_name != "django_rest_framework"
        and repo_name != "django_allauth"
        and repo_name != "django_debug_toolbar"
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
    command.extend(modules)
    if keyword:
        command.extend(["-k", keyword])
    click.echo(click.style(f"Running {' '.join(command)}", fg="blue"))
    if repo_name == "django_debug_toolbar":
        # For pytest to use correct settings file.
        os.environ["DJANGO_SETTINGS_MODULE"] = test_settings_map[repo_name][
            "settings_module"
        ]["tests"]
    subprocess.run(command, cwd=test_settings_map[repo_name]["cwd"])
