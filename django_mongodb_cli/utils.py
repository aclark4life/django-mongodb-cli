import click
import git
import os
import shutil
import sys
import toml
import re


from .config import project_dirs_map, test_settings_map


def add_remote(upstream_match, clone_path, repo_name):
    remote = f"https://github.com/{upstream_match.group(1)}/{repo_name}"
    repo = git.Repo(clone_path)
    try:
        repo.create_remote("upstream", remote)
    except git.exc.GitCommandError:
        click.echo("remote exists!")
    repo.remotes.upstream.fetch()
    repo.git.rebase("upstream/main")
    for remote in repo.remotes:
        print(f"{remote.name}: {remote.url}")


def apply_patches(app_type):
    """Apply a patch file to the specified project directory."""
    project_dir = project_dirs_map[app_type]
    patch_dir = os.path.join("patches", app_type)
    if os.path.exists(patch_dir):
        for patch_file in os.listdir(patch_dir):
            shutil.copyfile(
                os.path.join(patch_dir, patch_file),
                os.path.join(project_dir, patch_file),
            )
            click.echo(click.style(f"Applying patch {patch_file}", fg="blue"))
            # Ensure the repository is valid
            repo = git.Repo(project_dir)
            if not repo.bare:
                try:
                    # Apply the patch
                    repo.git.apply(patch_file)
                    click.echo(
                        f"Patch {os.path.basename(patch_file)} applied successfully."
                    )
                except Exception as e:
                    click.echo(f"Failed to apply patch: {e}")
                    return
            else:
                click.echo("Not a valid Git repository.")
                return
            click.echo(click.style("Patch applied", fg="green"))


def clone_from(repo_url, clone_path, branch):
    if not os.path.exists(clone_path):
        click.echo(f"Cloning {repo_url} into {clone_path} (branch: {branch})")
        try:
            git.Repo.clone_from(repo_url, clone_path, branch=branch)
        except git.exc.GitCommandError:
            try:
                git.Repo.clone_from(repo_url, clone_path)
            except git.exc.GitCommandError as e:
                click.echo(f"Failed to clone repository: {e}")
    else:
        click.echo(f"Skipping {repo_url} in {clone_path} (branch: {branch})")


def copy_mongo_apps(test_dir, app_type):
    """Copy the appropriate mongo_apps file based on the app type."""
    app_files = {
        "wagtail": "apps_wagtail.py",
        "django_filter": "apps_filter.py",
        "django_rest_framework": "apps_drf.py",
    }
    if app_type in app_files:
        click.echo(click.style(f"Copying mongo apps to {test_dir}", fg="blue"))
        shutil.copyfile(
            os.path.join("test_apps", app_files[app_type]),
            os.path.join(test_dir, "mongo_apps.py"),
        )


def copy_mongo_migrations(test_dir):
    """Copy mongo_migrations to the specified test directory."""
    click.echo(click.style(f"Copying mongo migrations to {test_dir}", fg="blue"))
    target_dir = os.path.join(test_dir, "mongo_migrations")
    if not os.path.exists(target_dir):
        shutil.copytree(
            os.path.join(
                "src",
                "django-project-templates",
                "project_template",
                "mongo_migrations",
            ),
            target_dir,
        )


def copy_test_settings(test_dir, app_type):
    """Retrieve settings for the specified app type."""
    test_settings = {
        "src": os.path.join("test_settings", test_settings_map[app_type]["src"]),
        "dest": os.path.join(test_dir, test_settings_map[app_type]["dest"]),
        "module": test_settings_map[app_type]["module"],
        "path": test_settings_map[app_type]["path"],
    }
    click.echo(click.style(f"Copying test settings to {test_dir}", fg="blue"))
    shutil.copyfile(test_settings["src"], test_settings["dest"])
    return test_settings


def delete_mongo_migrations(mongo_migrations, project_dir):
    click.echo(click.style(f"Deleting mongo migrations {mongo_migrations}", fg="blue"))
    shutil.rmtree(mongo_migrations, ignore_errors=True)
    for root, dirs, files in os.walk(project_dir):
        for dir_name in dirs:
            if dir_name == "migrations":
                dir_path = os.path.join(root, dir_name)
                click.echo(f"Removing: {dir_path}")
                shutil.rmtree(dir_path, ignore_errors=True)


def get_app_type(
    django_allauth, django_debug_toolbar, django_filter, django_rest_framework, wagtail
):
    """Determine the app type based on the specified options."""
    return (
        "django_allauth"
        if django_allauth
        else "django_debug_toolbar"
        if django_debug_toolbar
        else "django_filter"
        if django_filter
        else "django_rest_framework"
        if django_rest_framework
        else "wagtail"
        if wagtail
        else "default"
    )


def get_repos(pyproject_path):
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])

    url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")
    branch_pattern = re.compile(
        r"git\+ssh://git@github\.com/[^/]+/[^@]+@([a-zA-Z0-9_\-\.]+)\b"
    )
    upstream_pattern = re.compile(r"#\s*upstream:\s*([\w-]+)")
    return repos, url_pattern, branch_pattern, upstream_pattern


def get_management_command(command=None):
    REQUIRES_MANAGE_PY = {
        "createsuperuser",
        "migrate",
        "runserver",
        "shell",
        "startapp",
    }
    manage_py_exists = os.path.exists("manage.py")

    if not manage_py_exists and (command is None or command in REQUIRES_MANAGE_PY):
        exit(
            click.style(
                "manage.py is required to run this command. Please run this command in the project directory.",
                fg="red",
            )
        )

    base_command = (
        [sys.executable, "manage.py"] if manage_py_exists else ["django-admin"]
    )

    if command:
        full_command = base_command + [command]
        click.echo(
            click.style(
                f"Running command: {' '.join(full_command)}",
                fg="bright_cyan",
                reverse=True,
            )
        )
        return full_command

    return base_command


def pull(clone_path):
    repo = git.Repo(clone_path)
    repo.git.pull()
