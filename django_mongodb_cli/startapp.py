import click
import os
import subprocess


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing apps")
@click.argument("name", required=False)
def startapp(name, delete):
    """Run startapp command with the template from src/django-mongodb-app."""

    if delete:
        if os.path.exists("apps"):
            click.echo(subprocess.run(["rm", "-rf", "apps"]))
        else:
            click.echo("No apps directory found.")
        return

    if not os.path.exists("apps"):
        click.echo("Creating apps directory.")
        os.makedirs("apps")

    click.echo("Running startapp.")
    subprocess.run(
        [
            "django-admin",
            "startapp",
            name,
            "--template",
            os.path.join(os.path.join("..", "src", "django-mongodb-app")),
        ],
        cwd="apps",
    )
