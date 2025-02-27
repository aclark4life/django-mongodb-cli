import click
import git
import os
import shutil
import sys
import toml
import re
import subprocess


from .config import test_settings_map


def add_remote(upstream_match, clone_path, repo_name):
    remote = f"https://github.com/{upstream_match.group(1)}/{repo_name}"
    if os.path.exists(clone_path):
        repo = git.Repo(clone_path)
        try:
            repo.create_remote("upstream", remote)
            click.echo(f"Added remote {remote}")
        except git.exc.GitCommandError:
            click.echo("remote exists!")
        repo.remotes.upstream.fetch()
        try:
            repo.git.rebase("upstream/main")
        except git.exc.GitCommandError:
            click.echo("Failed to rebase")
        for remote in repo.remotes:
            click.echo(f"{remote.name}: {remote.url}")
    else:
        click.echo(f"Skipping {remote}")


def apply_patches(repo_name):
    """Apply a patch file to the specified project directory."""
    project_dir = test_settings_map[repo_name]["project_dir"]
    patch_dir = os.path.join("patches", repo_name)
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


def copy_mongo_apps(repo_name):
    """Copy the appropriate mongo_apps file based on the app type."""
    click.echo(click.style(f"Copying apps for {repo_name}", fg="blue"))
    if "apps" in test_settings_map[repo_name]:
        shutil.copyfile(
            os.path.join(test_settings_map[repo_name]["apps"]["src"]),
            os.path.join(test_settings_map[repo_name]["apps"]["target"]),
        )


def copy_mongo_migrations(repo_name):
    """Copy mongo_migrations to the specified test directory."""
    if not os.path.exists(test_settings_map[repo_name]["migrations_dir"]["target"]):
        click.echo(
            click.style(
                f"Copying migrations from {test_settings_map[repo_name]['migrations_dir']['src']} to {test_settings_map[repo_name]['migrations_dir']['target']}",
                fg="blue",
            )
        )
        shutil.copytree(
            test_settings_map[repo_name]["migrations_dir"]["src"],
            test_settings_map[repo_name]["migrations_dir"]["target"],
        )


def copy_mongo_settings(src, target):
    """Copy mongo_settings to the specified test directory."""
    click.echo(click.style(f"Copying {src} to {target}", fg="blue"))
    shutil.copyfile(src, target)


def delete_mongo_migrations(mongo_migrations, project_dir):
    click.echo(click.style(f"Deleting mongo migrations {mongo_migrations}", fg="blue"))
    shutil.rmtree(mongo_migrations, ignore_errors=True)
    for root, dirs, files in os.walk(project_dir):
        for dir_name in dirs:
            if dir_name == "migrations":
                dir_path = os.path.join(root, dir_name)
                click.echo(f"Removing: {dir_path}")
                shutil.rmtree(dir_path, ignore_errors=True)


def get_repo_name(
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
        else "django"
    )


def get_repos(pyproject_path):
    with open(pyproject_path, "r") as f:
        pyproject_data = toml.load(f)
    repos = pyproject_data.get("tool", {}).get("django_mongodb_cli", {}).get("dev", [])

    # url_pattern = re.compile(r"git\+ssh://[^@]+@([^@]+)")

    url_pattern = re.compile(r"git\+ssh://(?:[^@]+@)?([^/]+)/([^@]+)")

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
        return full_command

    return base_command


def install_dependencies(clone_path):
    if os.path.exists(os.path.join(clone_path, "pyproject.toml")):
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", clone_path])
    if os.path.exists(os.path.join(clone_path, "setup.py")):
        subprocess.run([sys.executable, "setup.py", "develop"], cwd=clone_path)
    if os.path.exists(os.path.join(clone_path, "requirements.txt")):
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=clone_path,
        )


def pull(clone_path):
    try:
        repo = git.Repo(clone_path)
        click.echo(f"Updating {clone_path}")
        repo.git.pull()
    except git.exc.NoSuchPathError:
        click.echo("Not a valid Git repository.")
