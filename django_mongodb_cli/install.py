import click
import os


@click.command()
@click.argument("name")
@click.option("-a", "--app", is_flag=True, help="Install app")
@click.option("-m", "--middleware", is_flag=True, help="Install middleware")
@click.option("-u", "--url", is_flag=True, help="Install url")
def install(name, app, url, middleware):
    """
    Add `name` to INSTALLED_APPS or MIDDLEWARE or urlpatterns `,
    if it is not already present.
    """

    settings_path = os.environ.get("DJANGO_SETTINGS_MODULE", "backend.settings")
    settings_path = settings_path.replace(".", "/") + ".py"
    urls_path = os.path.join("backend", "urls.py")
    import_statement = "from django.urls import include\n"

    if app:
        try:
            with open(settings_path, "r") as file:
                lines = file.readlines()

            installed_apps_started = False
            app_modified = False

            for i, line in enumerate(lines):
                if "INSTALLED_APPS" in line and "=" in line:
                    installed_apps_started = True

                if installed_apps_started and name in line:
                    click.echo(f"{name} is already installed.")
                    return

                if installed_apps_started and "]" in line:  # End of the list
                    lines.insert(i, f'    "{name}",\n')
                    app_modified = True
                    break

            if app_modified:
                with open(settings_path, "w") as file:
                    file.writelines(lines)
                click.echo(f"Added {name} to {settings_path}.")
            else:
                click.echo(f"Could not find INSTALLED_APPS in {settings_path}.")

        except Exception as e:
            click.echo(f"Error: {e}")

    elif url:
        try:
            with open(urls_path, "r") as file:
                lines = file.readlines()

            installed_urls_started = False
            urls_modified = False

            for i, line in enumerate(lines):
                # Check if the import statement is already in the file
                if import_statement not in lines:
                    # Find the position to insert (typically after other imports)
                    for idx, line in enumerate(lines):
                        if line.startswith("from") or line.startswith("import"):
                            continue
                        lines.insert(idx, import_statement)
                        break
                # Detect the urlpatterns list
                if "urlpatterns" in line and "=" in line:
                    installed_urls_started = True

                # Check if the app is already listed
                if installed_urls_started and name in line:
                    click.echo(f"{name} is already installed.")
                    return

                # Add the app at the end of the urlpatterns list
                if installed_urls_started and "]" in line:  # End of the list
                    lines.insert(i, f'    path("", include("{name}")),\n')
                    urls_modified = True
                    break

            if urls_modified:
                with open(urls_path, "w") as file:
                    file.writelines(lines)
                click.echo(f"Added {name} to urlpatterns in {urls_path}.")
            else:
                click.echo(f"Could not find urlpatterns in {urls_path}.")

        except Exception as e:
            click.echo(f"Error: {e}")
    elif middleware:
        try:
            with open(settings_path, "r") as file:
                lines = file.readlines()

            installed_middleware_started = False
            modified = False

            for i, line in enumerate(lines):
                if "MIDDLEWARE" in line and "=" in line:
                    installed_middleware_started = True

                if installed_middleware_started and name in line:
                    click.echo(f"{name} is already installed.")
                    return

                if installed_middleware_started and "]" in line:  # End of the list
                    lines.insert(i, f'    "{name}",\n')
                    modified = True
                    break

            if modified:
                with open(settings_path, "w") as file:
                    file.writelines(lines)
                click.echo(f"Added {name} to MIDDLEWARE in {settings_path}.")
            else:
                click.echo(f"Could not find MIDDLEWARE in {settings_path}.")

        except Exception as e:
            click.echo(f"Error: {e}")

    else:
        click.echo("Please specify either --app or --url or --middleware.")
        exit(1)
