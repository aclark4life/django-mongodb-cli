# app.py
import typer

app = typer.Typer()


@app.command()
def run():
    typer.echo("Running app!")


# import click
# import os
# import shutil
# import subprocess
#
#
# from .utils import get_management_command, random_app_name
#
#
# class App:
#    def __init__(self):
#        self.config = {}
#
#    def set_config(self, key, value):
#        self.config[key] = value
#
#    def __repr__(self):
#        return f"<App {self}>"
#
#
# pass_app = click.make_pass_decorator(App)
#
#
# @click.group(invoke_without_command=True)
# @click.pass_context
# def app(context):
#    """
#    Creates a Django app in ./apps with django-mongodb-backend configured.
#    """
#
#    context.obj = App()
#    if context.invoked_subcommand is None:
#        click.echo(context.get_help())
#        context.exit()
#
#
# @app.command()
# @click.argument("app_name", required=False)
# def start(app_name):
#    if not app_name:
#        app_name = random_app_name()
#
#    if not app_name.isidentifier():
#        raise click.UsageError(
#            f"App name '{app_name}' is not a valid Python identifier."
#        )
#
#    temp_path = app_name  # Django will create the app here temporarily
#    target_path = os.path.join("apps", app_name)
#
#    click.echo(f"Creating app '{app_name}' in ./apps")
#
#    os.makedirs("apps", exist_ok=True)
#
#    command = get_management_command("startapp")
#    subprocess.run(
#        command
#        + [
#            temp_path,
#            "--template",
#            os.path.join("templates", "app_template"),
#        ],
#        check=True,
#    )
#
#    # Move the generated app into ./apps/
#    shutil.move(temp_path, target_path)
