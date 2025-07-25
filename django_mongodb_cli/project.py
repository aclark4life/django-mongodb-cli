import typer

project = typer.Typer()


@project.command()
def run():
    typer.echo("Running app!")


# import click
# import os
# import shutil
# import subprocess
#
#
# from .utils import DELETE_DIRS_AND_FILES, get_management_command
#
#
# class Project:
#    def __init__(self):
#        self.config = {}
#
#    def set_config(self, key, value):
#        self.config[key] = value
#
#    def __repr__(self):
#        return f"<Proj {self}>"
#
#
# pass_project = click.make_pass_decorator(Project)
#
#
# @click.group(invoke_without_command=True)
# @click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
# @click.pass_context
# def project(context, delete):
#    context.obj = Project()
#
#    if delete:
#        for item, check_function in DELETE_DIRS_AND_FILES.items():
#            if check_function(item):
#                if os.path.isdir(item):
#                    shutil.rmtree(item)
#                    click.echo(f"Removed directory: {item}")
#                elif os.path.isfile(item):
#                    os.remove(item)
#                    click.echo(f"Removed file: {item}")
#            else:
#                click.echo(f"Skipping: {item} does not exist")
#        return
#
#    if context.invoked_subcommand is None:
#        click.echo(context.get_help())
#        context.exit()
#
#
# @project.command(context_settings={"ignore_unknown_options": True})
# @click.argument("args", nargs=-1)
# def manage(args):
#    """Run management commands."""
#
#    command = get_management_command()
#
#    subprocess.run(command + [*args])
#
#
# @project.command()
# def run():
#    if os.environ.get("MONGODB_URI"):
#        click.echo(os.environ["MONGODB_URI"])
#
#    command = get_management_command()
#
#    # Start npm install
#    subprocess.run(["npm", "install"], cwd="frontend")
#
#    # Start npm run watch
#    npm_process = subprocess.Popen(["npm", "run", "watch"], cwd="frontend")
#
#    # Start django-admin runserver
#    django_process = subprocess.Popen(command + ["runserver"])
#
#    # Wait for both processes to complete
#    npm_process.wait()
#    django_process.wait()
#
#
# @project.command()
# @click.option("-dj", "--django", is_flag=True, help="Use django mongodb template")
# @click.option("-w", "--wagtail", is_flag=True, help="Use wagtail mongodb template")
# @click.argument("project_name", required=False, default="backend")
# def new(
#    django,
#    wagtail,
#    project_name,
# ):
#    if os.path.exists("manage.py"):
#        click.echo("manage.py already exists")
#        return
#    template = None
#    django_admin = "django-admin"
#    startproject = "startproject"
#    startapp = "startapp"
#    if wagtail:
#        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
#        django_admin = "wagtail"
#        startproject = "start"
#    elif django:
#        template = os.path.join(os.path.join("src", "django-mongodb-project"))
#    if not template:
#        template = os.path.join(os.path.join("templates", "project_template"))
#    click.echo(f"Using template: {template}")
#    subprocess.run(
#        [
#            django_admin,
#            startproject,
#            project_name,
#            ".",
#            "--template",
#            template,
#        ]
#    )
#    frontend_template = os.path.join("templates", "frontend_template")
#    click.echo(f"Using template: {frontend_template}")
#    subprocess.run(
#        [
#            django_admin,
#            startproject,
#            "frontend",
#            ".",
#            "--template",
#            frontend_template,
#        ]
#    )
#    if not wagtail:
#        home_template = os.path.join("templates", "home_template")
#        click.echo(f"Using template: {home_template}")
#        subprocess.run(
#            [
#                django_admin,
#                startapp,
#                "home",
#                "--template",
#                home_template,
#            ]
#        )
#
#
# @project.command()
# def su():
#    try:
#        user_email = subprocess.check_output(
#            ["git", "config", "user.email"], text=True
#        ).strip()
#    except subprocess.CalledProcessError:
#        click.echo("Error: Unable to retrieve the user email from git config.")
#        return
#
#    os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
#
#    if os.environ.get("MONGODB_URI"):
#        click.echo(os.environ["MONGODB_URI"])
#    click.echo(f"User email: {user_email}")
#
#    command = get_management_command("createsuperuser")
#
#    subprocess.run(
#        command
#        + [
#            "--noinput",
#            "--username=admin",
#            f"--email={user_email}",
#        ]
#    )
