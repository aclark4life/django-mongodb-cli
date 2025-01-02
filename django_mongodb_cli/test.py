import click
import os
import shutil
import subprocess


def _copy_mongo_migrations(test_dir):
    click.echo(click.style("Copying mongo_migrations", fg="blue"))
    if not os.path.exists(os.path.join(test_dir, "mongo_migrations")):
        shutil.copytree(
            os.path.join("project_templates", "project_template", "mongo_migrations"),
            os.path.join(test_dir, "mongo_migrations"),
        )


def _copy_mongo_apps(test_dir):
    click.echo(click.style("Copying mongo_apps", fg="blue"))
    shutil.copyfile(
        "apps_wagtail.py",
        os.path.join(test_dir, "mongo_apps.py"),
    )


def _get_test_settings(test_dir, wagtail=False, django_filter=False):
    if wagtail:
        return [
            "settings_wagtail.py",
            os.path.join(test_dir, "mongo_settings.py"),
            "wagtail.test.mongo_settings",
            os.path.join("src", "wagtail"),
        ]
    elif django_filter:
        return [
            "settings_filter.py",
            os.path.join(test_dir, "mongo_settings.py"),
            "django_filters.tests.mongo_settings",
            os.path.join("src", "django-filter"),
        ]
    else:
        return [
            "settings_django.py",
            os.path.join(test_dir, "mongo_settings.py"),
            "mongo_settings",
            ".",
        ]


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-f", "--django-filter", help="Run Django Filter tests", is_flag=True)
@click.option("-l", "--list-tests", help="List tests", is_flag=True)
@click.option("-w", "--wagtail", help="Run Wagtail tests", is_flag=True)
def test(modules, keyword, list_tests, wagtail, django_filter):
    """
    Run `runtests.py` for Django or Wagtail.
    """
    click.echo(click.style("Running tests", fg="blue"))

    if wagtail:
        test_dir = os.path.join("src", "wagtail", "wagtail", "test")
        runtests_py = "./runtests.py"
        _copy_mongo_migrations(test_dir)
        _copy_mongo_apps(test_dir)
        test_settings = _get_test_settings(test_dir, wagtail=True)
    elif django_filter:
        test_dir = os.path.join("src", "django-filter", "tests")
        runtests_py = os.path.join("src", "django-filter", "runtests.py")
        test_settings = _get_test_settings(test_dir, django_filter=True)
    else:
        test_dir = os.path.join("src", "django", "tests")
        runtests_py = os.path.join(test_dir, "runtests.py")
        test_settings = _get_test_settings(test_dir)

    shutil.copyfile(
        test_settings[0],
        test_settings[1],
    )

    command = [runtests_py]
    command.extend(["--settings", test_settings[2]])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])
    command.extend(["--noinput"])

    if wagtail:
        command.extend(["wagtail.test." + module for module in modules])
    else:
        command.extend(modules)

    if list_tests:
        for module in sorted(os.listdir(test_dir)):
            click.echo(module)
        return

    click.echo(f"Running {' '.join(command)}")
    cwd = test_settings[3]
    click.echo(f"Working directory: {cwd}")
    if keyword:
        command.extend(["-k", keyword])

    subprocess.run(command, stdin=None, stdout=None, stderr=None, cwd=cwd)
