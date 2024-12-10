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
        runtests_py = os.path.join("src", "wagtail", "runtests.py")
        test_settings = [
            "settings.py",
            os.path.join("src", "wagtail", "wagtail", "test", "settings.py"),
        ]
    else:
        runtests_py = os.path.join("src", "django", "tests", "runtests.py")
        test_settings = [
            "mongodb_settings.py",
            os.path.join("src", "django", "tests", "mongodb_settings.py"),
        ]

    shutil.copyfile(
        test_settings[0],
        test_settings[1],
    )

    command = [runtests_py]
    command.extend(["--settings", "mongodb_settings"])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])
    command.extend(["--noinput"])
    command.extend(modules)

    if keyword:
        command.extend(["-k", keyword])

    subprocess.run(command, stdin=None, stdout=None, stderr=None)
