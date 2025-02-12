import click
import os
import subprocess

from .utils import (
    apply_patches,
    copy_mongo_migrations,
    copy_mongo_apps,
    copy_test_settings,
    test_dirs_map,
    runtests_py_map,
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
    click.echo(click.style("Running tests", fg="blue"))
    app_type = (
        "django_allauth"
        if django_allauth
        else "django_debug_toolbar"
        if django_debug_toolbar
        else "django_filter"
        if django_filter
        else "django_rest_framework"
        if django_rest_framework
        else "wagtail"
        if wagtail
        else "default"
    )
    test_dirs = test_dirs_map[app_type]
    if list_tests:
        for test_dir in test_dirs:
            for module in sorted(os.listdir(test_dir)):
                click.echo(module)
        return
    test_dir = test_dirs[0]
    apply_patches(app_type)
    copy_mongo_migrations(test_dir)
    copy_mongo_apps(test_dir, app_type)
    test_settings = copy_test_settings(test_dir, app_type)
    command = [runtests_py_map[app_type]]
    if (
        app_type != "django_rest_framework"
        and app_type != "django_allauth"
        and app_type != "django_debug_toolbar"
    ):
        command.extend(
            [
                "--settings",
                test_settings[2],
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
    click.echo(f"Running {' '.join(command)}")
    if app_type == "django_debug_toolbar":
        # Set the DJANGO_SETTINGS_MODULE environment variable
        # for pytest to use the correct settings file.
        os.environ["DJANGO_SETTINGS_MODULE"] = test_settings[2]
    cwd = test_settings[3]
    click.echo(f"Working directory: {cwd}")
    subprocess.run(command, cwd=cwd)
