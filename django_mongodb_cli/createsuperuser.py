import click
import os
import sys
import subprocess


@click.command()
def createsuperuser(mongo_single):
    """Create a superuser with the username 'admin' and the email from git config."""
    try:
        user_email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        click.echo(f"User email: {user_email}")
    except subprocess.CalledProcessError:
        click.echo("Error: Unable to retrieve the user email from git config.")
    os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
    subprocess.run(
        [
            sys.executable,
            "manage.py",
            "createsuperuser",
            "--noinput",
            "--username=admin",
            f"--email={user_email}",
        ]
    )
