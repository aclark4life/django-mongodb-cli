import click
import os
import shutil
import subprocess


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option("-w", "--wagtail", help="Run Wagtail tests", is_flag=True)
def runtests(modules, keyword, wagtail):
    """
    Run `runtests.py`
    """

    if wagtail:
        if not os.path.exists(
            os.path.join("src", "wagtail", "wagtail", "test", "mongo_migrations")
        ):
            shutil.copytree(
                os.path.join("project_template", "mongo_migrations"),
                os.path.join("src", "wagtail", "wagtail", "test", "mongo_migrations"),
            )
        shutil.copyfile(
            "mongo_apps.py",
            os.path.join("src", "wagtail", "wagtail", "test", "mongo_apps.py"),
        )
        runtests_py = "./runtests.py"
        test_settings = [
            "wagtail_settings.py",
            os.path.join("src", "wagtail", "wagtail", "test", "mongo_settings.py"),
            "wagtail.test.mongo_settings",
            os.path.join("src", "wagtail"),
        ]
    else:
        runtests_py = os.path.join("src", "django", "tests", "runtests.py")
        test_settings = [
            "django_settings.py",
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
