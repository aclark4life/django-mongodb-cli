import click
import os
import subprocess

from .utils import (
    copy_mongo_apps,
    copy_test_settings,
    delete_mongo_migrations,
    get_app_type,
    get_management_command,
    test_dirs_map,
)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-t",
    "--django-debug-toolbar",
    is_flag=True,
    help="Run makemigrations for Django Debug Toolbar.",
)
@click.option(
    "-r",
    "--django-rest-framework",
    is_flag=True,
    help="Run makemigrations for Django Rest Framework.",
)
@click.option(
    "-f", "--django-filter", is_flag=True, help="Run makemigrations for Django Filter."
)
@click.option(
    "-a",
    "--django-allauth",
    is_flag=True,
    help="Run makemigrations for Django Allauth.",
)
@click.option("-w", "--wagtail", is_flag=True, help="Run makemigrations for Wagtail.")
@click.option("-d", "--delete", is_flag=True, help="Delete migrations directory.")
@click.argument("args", nargs=-1)
def makemigrations(
    args,
    wagtail,
    delete,
    django_filter,
    django_rest_framework,
    django_allauth,
    django_debug_toolbar,
):
    """Run makemigrations."""

    command = get_management_command("makemigrations")

    app_type = get_app_type(
        django_allauth,
        django_debug_toolbar,
        django_filter,
        django_rest_framework,
        wagtail,
    )

    test_dirs = test_dirs_map[app_type]
    test_dir = test_dirs[0]

    if delete:
        if app_type == "wagtail":
            delete_mongo_migrations(
                os.path.join(test_dir, "mongo_migrations"),
                os.path.join("src", "wagtail"),
            )
            click.echo("Deleted migrations directory.")
            return

    copy_mongo_apps(test_dir, app_type)
    copy_test_settings(test_dir, app_type)
    subprocess.run(command + [*args])
