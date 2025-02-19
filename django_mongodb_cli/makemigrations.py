import click
import subprocess
import os


from .config import test_settings_map

from .utils import (
    copy_mongo_apps,
    copy_mongo_settings,
    get_app_type,
    get_management_command,
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
@click.argument("args", nargs=-1)
def makemigrations(
    args,
    wagtail,
    django_filter,
    django_rest_framework,
    django_allauth,
    django_debug_toolbar,
):
    """Run makemigrations."""
    app_type = get_app_type(
        django_allauth,
        django_debug_toolbar,
        django_filter,
        django_rest_framework,
        wagtail,
    )
    copy_mongo_apps(app_type)
    copy_mongo_settings(
        test_settings_map[app_type]["src"], test_settings_map[app_type]["target"]
    )
    command = get_management_command("makemigrations")
    command.extend(
        [
            "--settings",
            test_settings_map[app_type]["settings_module"],
        ]
    )
    if not app_type == "django_filter":
        command.extend(
            [
                "--pythonpath",
                os.path.join(os.getcwd(), test_settings_map[app_type]["cwd"]),
            ]
        )
    click.echo(f"Running command {' '.join(command)} {' '.join(args)}")
    subprocess.run(command + [*args])
