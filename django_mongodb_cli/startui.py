import click
import os
import shutil
import sys
import subprocess


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startui(delete):
    """Run webpack_init command to create frontend directory."""
    if delete:
        if os.path.isdir("frontend"):
            shutil.rmtree("frontend")
            print("Removed directory: frontend")
        else:
            print("Skipping: frontend does not exist")

        for frontend_file in [
            ".babelrc",
            ".browserslistrc",
            ".eslintrc",
            ".nvmrc",
            ".stylelintrc.json",
            "package-lock.json",
            "package.json",
            "postcss.config.js",
        ]:
            if os.path.isfile(frontend_file):
                os.remove(frontend_file)
                print(f"Removed file: {frontend_file}")
            else:
                print(f"Skipping: {frontend_file} does not exist")
        exit()

    click.echo(
        subprocess.run([sys.executable, "manage.py", "webpack_init", "--no-input"])
    )
