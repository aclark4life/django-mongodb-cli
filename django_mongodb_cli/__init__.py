import click
import git
import os
import re
import shutil
import sys
import subprocess
import toml


@click.command()
@click.argument(
    "pyproject_path", type=click.Path(exists=True), default="pyproject.toml"
)
@click.argument("clone_dir", type=click.Path(), default="src")
@click.option("-d", "--delete", is_flag=True, help="Delete existing checkouts")
@click.option("-u", "--update", is_flag=True, help="Update existing checkouts")
@click.option("-i", "--install", is_flag=True, help="Install checkouts")
def clone(pyproject_path, clone_dir, delete, update, install):
    """Clone repositories listed under [tool.django_mongodb_cli] dev in pyproject.toml."""
    if delete:
        if os.path.isdir("src"):
            shutil.rmtree("src")
            print("Removed directory: src")
        else:
            print("Skipping: src does not exist")
        exit()
    # Read and parse the pyproject.toml file
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)

    # Get the list of repositories
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])

    if not repos:
        click.echo("No repositories found under [tool.django_mongodb_cli] dev")
        return

    # Regex to extract the URL from the string
    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")
    branch_pattern = re.compile(r"@([^@]+)$")

    # Clone each repository
    for repo_entry in repos:
        url_match = url_pattern.search(repo_entry)
        branch_match = branch_pattern.search(repo_entry)

        if url_match:
            repo_url = url_match.group(0)
            repo_name = os.path.basename(repo_url)
            branch = branch_match.group(1) if branch_match else "main"
            clone_path = os.path.join(clone_dir, repo_name)

            if update:
                click.echo(f"Updating {repo_url} in {clone_path} (branch: {branch})")
                subprocess.run(["git", "pull"], cwd=clone_path)
                continue

            if not os.path.exists(clone_path):
                click.echo(f"Cloning {repo_url} into {clone_path} (branch: {branch})")
                try:
                    git.Repo.clone_from(repo_url, clone_path, branch=branch)
                except git.exc.GitCommandError as e:
                    click.echo(f"Failed to clone repository: {e}")
                pyproject_toml = os.path.join(clone_path, "pyproject.toml")
                if os.path.exists(pyproject_toml) and install:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-e", clone_path]
                    )
            else:
                click.echo(f"Skipping {repo_url} in {clone_path} (branch: {branch})")
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")
    click.echo("All repositories cloned successfully.")


@click.command()
def createsuperuser():
    """Create a superuser with the username 'admin' and the email from git config."""
    try:
        user_email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        print(f"User email: {user_email}")
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve the user email from git config.")
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


@click.command()
@click.argument("app_name", default="mongo_app")
def installapp(app_name):
    """
    Add `app_name` to the INSTALLED_APPS list in the Django settings file located at `settings_path`,
    if it is not already present.
    """
    settings_path = os.path.join("mongo_project", "settings.py")
    try:
        with open(settings_path, "r") as file:
            lines = file.readlines()

        installed_apps_started = False
        modified = False

        for i, line in enumerate(lines):
            # Detect the INSTALLED_APPS list
            if "INSTALLED_APPS" in line and "=" in line:
                installed_apps_started = True

            # Check if the app is already listed
            if installed_apps_started and app_name in line:
                click.echo(f"{app_name} is already installed.")
                return

            # Add the app at the end of the INSTALLED_APPS list
            if installed_apps_started and "]" in line:  # End of the list
                lines.insert(i, f'    "{app_name}",\n')
                modified = True
                break

        if modified:
            with open(settings_path, "w") as file:
                file.writelines(lines)
            click.echo(f"Added {app_name} to INSTALLED_APPS in {settings_path}.")
        else:
            click.echo(f"Could not find INSTALLED_APPS in {settings_path}.")

    except Exception as e:
        click.echo(f"Error: {e}")


@click.command()
@click.argument("middleware_name")
def installmiddleware(middleware_name):
    """
    Add `middleware_name` to the MIDDLEWARE list in the Django settings file located at settings_path,
    """
    settings_path = os.path.join("mongo_project", "settings.py")
    try:
        with open(settings_path, "r") as file:
            lines = file.readlines()

        installed_middleware_started = False
        modified = False

        for i, line in enumerate(lines):
            # Detect the INSTALLED_APPS list
            if "MIDDLEWARE" in line and "=" in line:
                installed_middleware_started = True

            # Check if the app is already listed
            if installed_middleware_started and middleware_name in line:
                click.echo(f"{middleware_name} is already installed.")
                return

            # Add the app at the end of the INSTALLED_APPS list
            if installed_middleware_started and "]" in line:  # End of the list
                lines.insert(i, f'    "{middleware_name}",\n')
                modified = True
                break

        if modified:
            with open(settings_path, "w") as file:
                file.writelines(lines)
            click.echo(f"Added {middleware_name} to MIDDLEWARE in {settings_path}.")
        else:
            click.echo(f"Could not find MIDDLEWARE in {settings_path}.")

    except Exception as e:
        click.echo(f"Error: {e}")


@click.command()
@click.argument("url_name")
def installurl(url_name):
    """
    Add `url_name` to the urlpatterns list in the Django urls file located at urls_path
    """
    settings_path = os.path.join("mongo_project", "urls.py")
    import_statement = "from django.urls import include\n"

    try:
        with open(settings_path, "r") as file:
            lines = file.readlines()

        installed_urls_started = False
        modified = False

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
            if installed_urls_started and url_name in line:
                click.echo(f"{url_name} is already installed.")
                return

            # Add the app at the end of the urlpatterns list
            if installed_urls_started and "]" in line:  # End of the list
                lines.insert(i, f'    path("", include("{url_name}")),\n')
                modified = True
                break

        if modified:
            with open(settings_path, "w") as file:
                file.writelines(lines)
            click.echo(f"Added {url_name} to urlpatterns in {settings_path}.")
        else:
            click.echo(f"Could not find urlpatterns in {settings_path}.")

    except Exception as e:
        click.echo(f"Error: {e}")


@click.command()
def runserver():
    """Start MongoDB and run the Django development server."""
    mongodb = subprocess.Popen(["mongo-launch", "single"])
    subprocess.run([sys.executable, "manage.py", "runserver"])
    mongodb.terminate()


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startapp(delete):
    """Run startapp command with the template from src/django-mongodb-app."""
    if delete:
        if os.path.isdir("mongo_app"):
            shutil.rmtree("mongo_app")
            print("Removed directory: mongo_app")
        else:
            print("Skipping: mongo_app does not exist")
        exit()
    if os.path.exists("manage.py"):
        click.echo(
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "startapp",
                    "mongo_app",
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )
    else:
        click.echo(
            subprocess.run(
                [
                    "django-admin",
                    "startapp",
                    "mongo_app",
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
def startproject(delete):
    """Run startproject command with the template from src/django-mongodb-project."""
    if delete:
        if os.path.isdir("mongo_project"):
            shutil.rmtree("mongo_project")
            print("Removed directory: mongo_project")
        else:
            print("Skipping: mongo_project does not exist")

        if os.path.isdir("mongo_migrations"):
            shutil.rmtree("mongo_migrations")
            print("Removed directory: mongo_migrations")
        else:
            print("Skipping: mongo_migrations does not exist")

        if os.path.isfile("manage.py"):
            os.remove("manage.py")
            print("Removed file: manage.py")
        else:
            print("Skipping: manage.py does not exist")

        exit()
    click.echo(
        subprocess.run(
            [
                "django-admin",
                "startproject",
                "mongo_project",
                ".",
                "--template",
                os.path.join(os.path.join("src", "django-mongodb-project")),
            ]
        )
    )


@click.command()
@click.argument("modules", nargs=-1)
@click.option("-k", "--keyword", help="Filter tests by keyword")
@click.option(
    "-l", "--list-tests", default=False, is_flag=True, help="List available tests"
)
@click.option(
    "--dry-run", is_flag=True, help="Perform a dry run without executing tests"
)
def test(modules, keyword, list_tests, dry_run):
    """
    Run tests for specified modules with an optional keyword filter.
    """
    if list_tests:
        click.echo(subprocess.run(["ls", os.path.join("src", "django", "tests")]))
        click.echo(
            subprocess.run(["ls", os.path.join("src", "django-mongodb", "tests")])
        )
        exit()

    shutil.copyfile(
        "mongodb_settings.py",
        "src/django/tests/mongodb_settings.py",
    )

    command = ["src/django/tests/runtests.py"]
    command.extend(["--settings", "mongodb_settings"])
    command.extend(["--parallel", "1"])
    command.extend(["--verbosity", "3"])
    command.extend(["--debug-sql"])
    command.extend(["--noinput"])

    # Add modules to the command
    command.extend(modules)

    # Add keyword filter if provided
    if keyword:
        command.extend(["-k", keyword])

    click.echo(f"Running command: {' '.join(command)}")
    if dry_run:
        exit()

    # Start MongoDB
    mongodb = subprocess.Popen(["mongo-launch", "single"])

    # Execute the test command
    subprocess.run(command, stdin=None, stdout=None, stderr=None)

    # Terminate MongoDB
    mongodb.terminate()


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(installapp)
cli.add_command(installmiddleware)
cli.add_command(installurl)
cli.add_command(runserver)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(test)
