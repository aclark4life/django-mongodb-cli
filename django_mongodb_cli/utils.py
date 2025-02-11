import click
import os
import shutil
import toml
import re

from git import Repo


runtests_py_map = {
    "default": os.path.join("src", "django", "tests", "runtests.py"),
    "django_allauth": "tox",
    "django_debug_toolbar": "pytest",
    "django_filter": "./runtests.py",
    "django_rest_framework": "./runtests.py",
    "wagtail": "./runtests.py",
}

test_dirs_map = {
    "default": [
        os.path.join("src", "django", "tests"),
        os.path.join("src", "django-mongodb-backend", "tests"),
    ],
    "django_allauth": [os.path.join("src", "django-allauth", "tests")],
    "django_debug_toolbar": [os.path.join("src", "django-debug-toolbar", "tests")],
    "django_filter": [os.path.join("src", "django-filter", "tests")],
    "django_rest_framework": [os.path.join("src", "django-rest-framework", "tests")],
    "wagtail": [
        os.path.join("src", "wagtail", "wagtail", "test"),
        os.path.join("src", "wagtail", "wagtail", "tests"),
    ],
}

project_dirs_map = {
    "default": os.path.join("src", "django"),
    "django_allauth": os.path.join("src", "django-allauth"),
    "django_debug_toolbar": os.path.join("src", "django-debug-toolbar"),
    "django_filter": os.path.join("src", "django-filter"),
    "django_rest_framework": os.path.join("src", "django-rest-framework"),
    "wagtail": os.path.join("src", "wagtail"),
}


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
            repo = Repo(project_dir)
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
    settings_map = {
        "default": [
            "settings_django.py",
            "mongo_settings.py",
            "mongo_settings",
            ".",
        ],
        "django_allauth": [
            "settings_allauth_regular.py",
            "mongo_settings.py",
            "tests.mongo_settings",
            os.path.join("src", "django-allauth"),
        ],
        "django_debug_toolbar": [
            "settings_debug_toolbar.py",
            "mongo_settings.py",
            "tests.mongo_settings",
            os.path.join("src", "django-debug-toolbar"),
        ],
        "django_filter": [
            "settings_filter.py",
            "mongo_settings.py",
            "tests.mongo_settings",
            os.path.join("src", "django-filter"),
        ],
        "django_rest_framework": [
            "settings_drf.py",
            "conftest.py",
            "tests.conftest",
            os.path.join("src", "django-rest-framework"),
        ],
        "wagtail": [
            "settings_wagtail.py",
            "mongo_settings.py",
            "wagtail.test.mongo_settings",
            os.path.join("src", "wagtail"),
        ],
    }
    test_settings = [
        os.path.join("test_settings", settings_map[app_type][0]),
        os.path.join(test_dir, settings_map[app_type][1]),
        settings_map[app_type][2],
        settings_map[app_type][3],
    ]
    click.echo(click.style(f"Copying test settings to {test_dir}", fg="blue"))
    shutil.copyfile(test_settings[0], test_settings[1])
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
