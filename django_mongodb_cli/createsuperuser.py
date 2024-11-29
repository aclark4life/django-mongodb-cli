import click
import os
import sys
import subprocess
from .utils import mongo_launch


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
def createsuperuser(mongo_single):
    """Create a superuser with the username 'admin' and the email from git config."""
    try:
        user_email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        print(f"User email: {user_email}")
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve the user email from git config.")
    os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
    if mongo_single:
        mongodb = subprocess.Popen(mongo_launch())
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
    if mongo_single:
        mongodb.terminate()
