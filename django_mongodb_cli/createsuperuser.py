import click
import os
import sys
import subprocess


@click.command()
def createsuperuser():
    """Create a superuser with the username 'admin' and the email from git config."""
    try:
        user_email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        click.echo("Error: Unable to retrieve the user email from git config.")
        return

    os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"

    click.echo(os.environ["MONGODB_URI"])
    click.echo(f"User email: {user_email}")

    if os.path.exists("manage.py"):
        command = os.path.join(sys.executable, "manage.py")
    else:
        command = "django-admin"

    subprocess.run(
        [
            command,
            "createsuperuser",
            "--noinput",
            "--username=admin",
            f"--email={user_email}",
        ]
    )
