import click
import os
import sys
import subprocess

from .utils import (
    copy_mongo_apps,
    copy_test_settings,
    delete_mongo_migrations,
    test_dirs_map,
)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("-w", "--wagtail", is_flag=True, help="Run makemigrations for Wagtail.")
@click.option("-d", "--delete", is_flag=True, help="Delete migrations directory.")
@click.argument("args", nargs=-1)
def makemigrations(args, wagtail, delete):
    """Run makemigrations."""

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py", "makemigrations"]
    else:
        command = ["django-admin", "makemigrations"]  # Use a list for consistency

    app_type = (
        "wagtail"
        if wagtail
        # else "django_filter"
        # if django_filter
        # else "django_rest_framework"
        # if django_rest_framework
        else "default"
    )

    test_dirs = test_dirs_map[app_type]
    test_dir = test_dirs[0]

    copy_mongo_apps(test_dir, app_type)
    copy_test_settings(test_dir, app_type)

    if app_type == "wagtail":
        if delete:
            delete_mongo_migrations(
                os.path.join(test_dir, "mongo_migrations"),
                os.path.join("src", "wagtail"),
            )
        os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail.test.mongo_settings"

    subprocess.run(command + [*args])
