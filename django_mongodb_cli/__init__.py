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
@click.option("-f", "--fetch", is_flag=True, help="Fetch from remotes")
@click.option("-i", "--install", is_flag=True, help="Install checkouts")
@click.option("-l", "--list-checkouts", is_flag=True, help="List checkouts")
@click.option("-r", "--remote", is_flag=True, help="Add upstream remotes")
@click.option("-u", "--update", is_flag=True, help="Update existing checkouts")
@click.option("-b", "--sphinx-build", is_flag=True, help="Build Sphinx documentation")
@click.option("-s", "--sphinx-serve", is_flag=True, help="Serve Sphinx documentation")
def clone(
    pyproject_path,
    clone_dir,
    delete,
    update,
    install,
    list_checkouts,
    remote,
    fetch,
    sphinx_build,
    sphinx_serve,
):
    """Clone repositories in `dev` in [tool.django_mongodb_cli] in pyproject.toml."""
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

    if list_checkouts:
        print("\n".join(repos))
        exit()

    # Regex to extract the URL from the string
    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")
    branch_pattern = re.compile(
        r"git\+ssh://git@github\.com/[^/]+/[^@]+@([a-zA-Z0-9_\-\.]+)\b"
    )
    upstream_pattern = re.compile(r"#\s*upstream:\s*([\w-]+)")

    # Clone each repository
    for repo_entry in repos:
        url_match = url_pattern.search(repo_entry)
        branch_match = branch_pattern.search(repo_entry)
        upstream_match = upstream_pattern.search(repo_entry)

        if url_match:
            repo_url = url_match.group(0)
            repo_name = os.path.basename(repo_url)
            branch = branch_match.group(1) if branch_match else "main"
            clone_path = os.path.join(clone_dir, repo_name)
            pyproject_toml = os.path.join(clone_path, "pyproject.toml")

            if update:
                click.echo(f"Updating {repo_url} in {clone_path} (branch: {branch})")
                subprocess.run(["git", "pull"], cwd=clone_path)

            if install and os.path.exists(pyproject_toml):
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", clone_path]
                )

            if not os.path.exists(clone_path):
                click.echo(f"Cloning {repo_url} into {clone_path} (branch: {branch})")
                try:
                    git.Repo.clone_from(repo_url, clone_path, branch=branch)
                    subprocess.run(["pre-commit", "install"], cwd=clone_path)
                except git.exc.GitCommandError as e:
                    click.echo(f"Failed to clone repository: {e}")
            else:
                click.echo(f"Skipping {repo_url} in {clone_path} (branch: {branch})")

            if remote and upstream_match:
                remote = f"https://github.com/{upstream_match.group(1)}/{repo_name}"
                subprocess.run(
                    ["git", "remote", "add", "upstream", remote], cwd=clone_path
                )
                subprocess.run(["git", "remote", "-v", "show"], cwd=clone_path)

            if fetch:
                subprocess.run(["git", "fetch", "upstream"], cwd=clone_path)

            if sphinx_build:
                try:
                    sphinx_path = os.path.join(clone_path, "docs", "source")
                    subprocess.run(
                        [
                            "sphinx-build",
                            ".",
                            "_build",
                        ],
                        cwd=sphinx_path,
                    )
                except FileNotFoundError:
                    click.echo(f"Invalid sphinx path: {sphinx_path}")
            if sphinx_serve:
                try:
                    sphinx_path = os.path.join(clone_path, "docs", "source", "_build")
                    subprocess.run(
                        [
                            "python",
                            "-m",
                            "http.server",
                        ],
                        cwd=sphinx_path,
                    )
                except FileNotFoundError:
                    click.echo(f"Invalid sphinx path: {sphinx_path}")
        else:
            click.echo(f"Invalid repository entry: {repo_entry}")
    click.echo("All repositories cloned successfully.")


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
        mongodb = subprocess.Popen(["mongo-launch", "single"])
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
    settings_path = os.path.join("backend", "settings.py")
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


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
def migrate(mongo_single):
    """Run Django migrations."""
    if mongo_single:
        mongodb = subprocess.Popen(["mongo-launch", "single"])
    subprocess.run([sys.executable, "manage.py", "migrate"])
    if mongo_single:
        mongodb.terminate()


@click.command()
@click.option(
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
def runserver(mongo_single):
    """Start MongoDB and run the Django development server."""
    if mongo_single:
        mongodb = subprocess.Popen(["mongo-launch", "single"])
    subprocess.run([sys.executable, "manage.py", "runserver"])
    if mongo_single:
        mongodb.terminate()


@click.command()
@click.argument("name")
def startapp(name):
    """Run startapp command with the template from src/django-mongodb-app."""
    if os.path.exists("manage.py"):
        click.echo(
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "startapp",
                    name,
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
                    name,
                    "--template",
                    os.path.join(os.path.join("src", "django-mongodb-app")),
                ]
            )
        )


@click.command()
@click.option("-d", "--delete", is_flag=True, help="Delete existing project files")
@click.option("-f", "--frontend", is_flag=True, help="Initialize frontend")
@click.option("-w", "--wagtail-project", is_flag=True, help="Use wagtail template")
@click.option(
    "-y", "--ye-olde-django-project", is_flag=True, help="Use the ye olde template"
)
def startproject(delete, frontend, wagtail_project):
    """Run startproject command with the template from src/django-mongodb-project."""
    if delete:
        if os.path.isdir("backend"):
            shutil.rmtree("backend")
            print("Removed directory: backend")
        else:
            print("Skipping: backend does not exist")

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

        if os.path.isdir("frontend"):
            shutil.rmtree("frontend")
            print("Removed directory: frontend")
        else:
            print("Skipping: frontend does not exist")

        if os.path.isdir("apps"):
            shutil.rmtree("apps")
            print("Removed directory: apps")
        else:
            print("Skipping: apps does not exist")

        exit()

    if frontend:
        click.echo(
            subprocess.run([sys.executable, "manage.py", "webpack_init", "--no-input"])
        )
        exit()

    if wagtail_project:
        template = os.path.join(os.path.join("src", "wagtail-mongodb-project"))
    else:
        template = os.path.join(os.path.join("src", "django-mongodb-project"))

    click.echo(
        subprocess.run(
            [
                "django-admin",
                "startproject",
                "backend",
                ".",
                "--template",
                template,
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
    "-m", "--mongo-single", is_flag=True, help="Launch a single MongoDB instance"
)
@click.option(
    "--dry-run", is_flag=True, help="Perform a dry run without executing tests"
)
def test(modules, keyword, list_tests, dry_run, mongo_single):
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

    if mongo_single:
        # Start MongoDB
        mongodb = subprocess.Popen(["mongo-launch", "single"])

    # Execute the test command
    subprocess.run(command, stdin=None, stdout=None, stderr=None)

    if mongo_single:
        # Terminate MongoDB
        mongodb.terminate()


@click.group()
def cli():
    pass


cli.add_command(clone)
cli.add_command(createsuperuser)
cli.add_command(install)
cli.add_command(migrate)
cli.add_command(runserver)
cli.add_command(startapp)
cli.add_command(startproject)
cli.add_command(test)
