import click
import os
import shutil
import subprocess


def copy_mongo_apps(test_dir, app_type):
    """Copy the appropriate mongo_apps file based on the app type."""
    app_files = {
        "wagtail": "apps_wagtail.py",
        "django_filter": "apps_filter.py",
        "django_rest_framework": "apps_drf.py",
    }
    if app_type in app_files:
        click.echo(click.style(f"Copying mongo_apps to {app_type}", fg="blue"))
        shutil.copyfile(
            os.path.join("test_apps", app_files[app_type]),
            os.path.join(test_dir, "mongo_apps.py"),
        )


def copy_mongo_migrations(test_dir):
    """Copy mongo_migrations to the specified test directory."""
    click.echo(click.style("Copying mongo_migrations", fg="blue"))
    target_dir = os.path.join(test_dir, "mongo_migrations")
    if not os.path.exists(target_dir):
        shutil.copytree(
            os.path.join("project_templates", "project_template", "mongo_migrations"),
            target_dir,
        )


def get_test_settings(test_dir, app_type):
    """Retrieve settings for the specified app type."""
    settings_map = {
        "wagtail": [
            "settings_wagtail.py",
            "mongo_settings.py",
            "wagtail.test.mongo_settings",
            os.path.join("src", "wagtail"),
        ],
        "django_filter": [
            "settings_filter.py",
            "mongo_settings.py",
            "tests.mongo_settings",
            os.path.join("src", "django-filter"),
        ],
        "django_rest_framework": [
            "settings_drf.py",
            "conftest.py",
            "tests.conftest",
            os.path.join("src", "django-rest-framework"),
        ],
        "default": [
            "settings_django.py",
            "mongo_settings.py",
            "mongo_settings",
            ".",
        ],
    }
    return [
        os.path.join("test_settings", settings_map[app_type][0]),
        os.path.join(test_dir, settings_map[app_type][1]),
        settings_map[app_type][2],
        settings_map[app_type][3],
    ]


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

    test_dirs_map = {
        "wagtail": [
            os.path.join("src", "wagtail", "wagtail", "test"),
            os.path.join("src", "wagtail", "wagtail", "tests"),
        ],
        "django_filter": [os.path.join("src", "django-filter", "tests")],
        "django_rest_framework": [
            os.path.join("src", "django-rest-framework", "tests")
        ],
        "default": [
            os.path.join("src", "django", "tests"),
            os.path.join("src", "django-mongodb-backend", "tests"),
        ],
    }

    test_dirs = test_dirs_map[app_type]
    main_test_dir = test_dirs[0]

    copy_mongo_migrations(main_test_dir)
    copy_mongo_apps(main_test_dir, app_type)
    test_settings = get_test_settings(main_test_dir, app_type)

    shutil.copyfile(test_settings[0], test_settings[1])

    runtests_py_map = {
        "wagtail": "./runtests.py",
        "django_filter": "./runtests.py",
        "django_rest_framework": "./runtests.py",
        "default": os.path.join("src", "django", "tests", "runtests.py"),
    }

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
