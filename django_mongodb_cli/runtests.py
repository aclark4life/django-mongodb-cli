import click
import os
import subprocess

from .utils import (
    copy_mongo_migrations,
    copy_mongo_apps,
    copy_test_settings,
    test_dirs_map,
    runtests_py_map,
)


@click.command()
@click.argument("modules", nargs=-1)
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
    modules, keyword, list_tests, wagtail, django_filter, django_rest_framework
):
    """
    Run `runtests.py` for Django or Wagtail.
    """
    click.echo(click.style("Running tests", fg="blue"))

    app_type = (
        "wagtail"
        if wagtail
        else "django_filter"
        if django_filter
        else "django_rest_framework"
        if django_rest_framework
        else "default"
    )

    test_dirs = test_dirs_map[app_type]
    main_test_dir = test_dirs[0]

    copy_mongo_migrations(main_test_dir)
    copy_mongo_apps(main_test_dir, app_type)
    test_settings = copy_test_settings(main_test_dir, app_type)

    command = [runtests_py_map[app_type]]

    if app_type != "django_rest_framework":
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

    if list_tests:
        for test_dir in test_dirs:
            for module in sorted(os.listdir(test_dir)):
                click.echo(module)
        return

    click.echo(f"Running {' '.join(command)}")
    cwd = test_settings[3]
    click.echo(f"Working directory: {cwd}")
    if keyword:
        command.extend(["-k", keyword])

    subprocess.run(command, cwd=cwd)
