import click
import os
import subprocess

from .utils import (
    copy_mongo_apps,
    copy_test_settings,
    delete_mongo_migrations,
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

    command = get_management_command()

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

    if app_type == "wagtail":
        os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail.test.mongo_settings"
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mongo_settings"

    subprocess.run(command + [*args])
