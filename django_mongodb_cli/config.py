import os

test_settings_map = {
    "django": {
        "cwd": os.path.join("src", "django", "tests"),
        "command": "./runtests.py",
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-project-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": os.path.join("src", "django", "tests"),
        },
        "project_dir": os.path.join("src", "django"),
        "settings_file": {
            "test": {
                "src": os.path.join("stage", "settings", "settings_django.py"),
                "target": os.path.join("src", "django", "tests", "mongo_settings.py"),
            },
            "migrate": {
                "src": os.path.join("stage", "settings", "settings_django.py"),
                "target": os.path.join("src", "django", "tests", "mongo_settings.py"),
            },
        },
        "settings_module": {
            "test": "mongo_settings",
            "migrate": "mongo_settings",
        },
        "target": os.path.join("src", "django", "tests", "mongo_settings.py"),
        "test_dirs": [
            os.path.join("src", "django", "tests"),
            os.path.join("src", "django-mongodb-backend", "tests"),
        ],
    },
    "django_filter": {
        "apps": {
            "src": os.path.join("stage", "apps", "apps_filter.py"),
            "target": os.path.join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django-filter"),
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-project-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": os.path.join("src", "django-filter", "tests"),
        },
        "project_dir": os.path.join("src", "django-filter"),
        "settings_file": {
            "test": {
                "src": os.path.join("stage", "settings", "settings_filter.py"),
                "target": os.path.join("src", "django-filter", "tests", "settings.py"),
            },
            "migrate": {
                "src": os.path.join("stage", "settings", "settings_filter.py"),
                "target": os.path.join("src", "django-filter", "tests", "settings.py"),
            },
        },
        "settings_module": {
            "test": "tests.settings",
            "migrate": "tests.settings",
        },
        "test_dirs": [os.path.join("src", "django-filter", "tests")],
    },
    "django_rest_framework": {
        "apps": {
            "src": os.path.join("stage", "apps", "apps_drf.py"),
            "target": os.path.join(
                "src", "django-rest-framework", "tests", "mongo_apps.py"
            ),
        },
        "migrations_dir": {
            "src": os.path.join("src", "django-mongodb-project", "mongo_migrations"),
            "target": os.path.join(
                "src", "django-rest-framework", "tests", "mongo_migrations"
            ),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django-rest-framework"),
        "project_dir": os.path.join("src", "django-rest-framework"),
        "settings_file": {
            "test": {
                "src": os.path.join("stage", "settings", "settings_drf.py"),
                "target": os.path.join(
                    "src", "django-rest-framework", "tests", "conftest.py"
                ),
            },
            "migrate": {
                "src": os.path.join("stage", "settings", "settings_drf_migrate.py"),
                "target": os.path.join(
                    "src", "django-rest-framework", "tests", "conftest.py"
                ),
            },
        },
        "settings_module": {
            "test": "tests.conftest",
            "migrate": "tests.conftest",
        },
        "test_dirs": [os.path.join("src", "django-rest-framework", "tests")],
    },
    "wagtail": {
        "apps": {
            "src": os.path.join("stage", "apps", "apps_wagtail.py"),
            "target": os.path.join(
                "src", "wagtail", "wagtail", "test", "mongo_apps.py"
            ),
        },
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-project-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": os.path.join(
                "src", "wagtail", "wagtail", "test", "mongo_migrations"
            ),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "wagtail"),
        "project_dir": os.path.join("src", "wagtail"),
        "settings_file": {
            "test": {
                "src": os.path.join("stage", "settings", "settings_wagtail.py"),
                "target": os.path.join(
                    "src", "wagtail", "wagtail", "tests", "mongo_settings.py"
                ),
            },
        },
        "settings_module": {
            "test": "wagtail.tests.mongo_settings",
            "migrate": "wagtail.tests.mongo_settings",
        },
        "test_dirs": [os.path.join("src", "wagtail", "wagtail", "tests")],
    },
    "django_allauth": {
        "command": "tox",
        "project_dir": os.path.join("src", "django-allauth"),
        "settings_module": "mongo_settings",
        "src": os.path.join("stage", "settings", "settings_allauth_regular.py"),
        "target": "mongo_settings.py",
        "test_dirs": ["tests"],
    },
    "django_debug_toolbar": {
        "command": "pytest",
        "project_dir": os.path.join("src", "django-debug-toolbar"),
        "settings_module": "mongo_settings",
        "src": os.path.join("stage", "settings", "settings_debug_toolbar.py"),
        "target": "mongo_settings.py",
        "test_dirs": ["tests"],
    },
}
