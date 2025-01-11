import click
import os
import sys
import subprocess


@click.command()
def runserver():
    """Start the Django development server."""

    if os.environ.get("MONGODB_URI"):
        click.echo(os.environ["MONGODB_URI"])

    if os.path.exists("manage.py"):
        command = [sys.executable, "manage.py"]
    else:
        command = ["django-admin"]  # Use a list for consistency

    # Start npm install
    subprocess.Popen(["npm", "install"])

    # Start npm run watch
    npm_process = subprocess.Popen(["npm", "run", "watch"])

    # Start django-admin runserver
    django_process = subprocess.Popen(command + ["runserver"])

    # Wait for both processes to complete
    npm_process.wait()
    django_process.wait()
