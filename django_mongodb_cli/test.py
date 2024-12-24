import click
import os
import shutil
import subprocess


def _copy_mongo_migrations():
    click.echo(click.style("Copying mongo_migrations", fg="blue"))
    if not os.path.exists(
        os.path.join("src", "wagtail", "wagtail", "test", "mongo_migrations")
    ):
        shutil.copytree(
            os.path.join("project_template", "mongo_migrations"),
            os.path.join("src", "wagtail", "wagtail", "test", "mongo_migrations"),
        )


def _copy_mongo_apps():
    click.echo(click.style("Copying mongo_apps", fg="blue"))
    shutil.copyfile(
        "apps_wagtail.py",
        os.path.join("src", "wagtail", "wagtail", "test", "mongo_apps.py"),
    )


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-w", "--wagtail", help="Run Wagtail tests", is_flag=True)
def test(modules, keyword, wagtail):
    """
    Run `runtests.py`
    """
    click.echo(click.style("Running tests", fg="blue"))

    if wagtail:
        _copy_mongo_migrations()
        _copy_mongo_apps()
        runtests_py = "./runtests.py"
        test_settings = [
            "settings_wagtail.py",
            os.path.join("src", "wagtail", "wagtail", "test", "mongo_settings.py"),
            "wagtail.test.mongo_settings",
            os.path.join("src", "wagtail"),
        ]
    else:
        runtests_py = os.path.join("src", "django", "tests", "runtests.py")
        test_settings = [
            "settings_django.py",
            os.path.join("src", "django", "tests", "mongo_settings.py"),
            "mongo_settings",
            ".",
        ]

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
    command.extend(modules)
    click.echo(f"Running {' '.join(command)}")

    cwd = test_settings[3]
    click.echo(f"Working directory: {cwd}")
    if keyword:
        command.extend(["-k", keyword])

    subprocess.run(command, stdin=None, stdout=None, stderr=None, cwd=cwd)
