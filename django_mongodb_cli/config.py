import os

test_settings_map = {
    "django": {
        "cwd": os.path.join("src", "django", "tests"),
        "command": "./runtests.py",
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": os.path.join("src", "django", "tests"),
        },
        "project_dir": os.path.join("src", "django"),
        "settings_file": {
            "test": {
                "src": os.path.join("settings", "django_settings.py"),
                "target": os.path.join("src", "django", "tests", "mongo_settings.py"),
            },
            "migrate": {
                "src": os.path.join("settings", "django_settings.py"),
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
    "django-filter": {
        "apps": {
            "src": os.path.join("settings", "filter_apps.py"),
            "target": os.path.join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django-filter"),
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": os.path.join("src", "django-filter", "tests", "mongo_migrations"),
        },
        "project_dir": os.path.join("src", "django-filter"),
        "settings_file": {
            "test": {
                "src": os.path.join("settings", "filter_settings.py"),
                "target": os.path.join("src", "django-filter", "tests", "settings.py"),
            },
            "migrate": {
                "src": os.path.join("settings", "filter_settings.py"),
                "target": os.path.join("src", "django-filter", "tests", "settings.py"),
            },
        },
        "settings_module": {
            "test": "tests.settings",
            "migrate": "tests.settings",
        },
        "test_dirs": [os.path.join("src", "django-filter", "tests")],
    },
    "django-rest-framework": {
        "apps": {
            "src": os.path.join("settings", "rest_framework_apps.py"),
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
                "src": os.path.join("settings", "rest_framework_settings.py"),
                "target": os.path.join(
                    "src", "django-rest-framework", "tests", "conftest.py"
                ),
            },
            "migrate": {
                "src": os.path.join("settings", "rest_framework_migrate.py"),
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
            "src": os.path.join("settings", "apps_wagtail.py"),
            "target": os.path.join(
                "src", "wagtail", "wagtail", "test", "mongo_apps.py"
            ),
        },
        "migrations_dir": {
            "src": os.path.join(
                "src",
                "django-mongodb-templates",
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
                "src": os.path.join("settings", "settings_wagtail.py"),
                "target": os.path.join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
            "migrate": {
                "src": os.path.join("settings", "settings_wagtail.py"),
                "target": os.path.join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
        },
        "settings_module": {
            "test": "wagtail.test.mongo_settings",
            "migrate": "wagtail.test.mongo_settings",
        },
        "test_dirs": [
            os.path.join("src", "wagtail", "wagtail", "tests"),
            os.path.join("src", "wagtail", "wagtail", "test"),
        ],
    },
    "django-debug-toolbar": {
        "apps": {
            "src": os.path.join("settings", "debug_toolbar_apps.py"),
            "target": os.path.join(
                "src", "django-debug-toolbar", "debug_toolbar", "mongo_apps.py"
            ),
        },
        "command": "python",
        "cwd": os.path.join("src", "django-debug-toolbar"),
        "project_dir": os.path.join("src", "django-debug-toolbar"),
        "settings_file": {
            "test": {
                "src": os.path.join("settings", "debug_toolbar_settings.py"),
                "target": os.path.join(
                    "src", "django-debug-toolbar", "debug_toolbar", "mongo_settings.py"
                ),
            },
            "migrate": {
                "src": os.path.join("settings", "debug_toolbar_settings.py"),
                "target": os.path.join(
                    "src", "django-debug-toolbar", "debug_toolbar", "mongo_settings.py"
                ),
            },
        },
        "settings_module": {
            "test": "debug_toolbar.mongo_settings",
            "migrate": "debug_toolbar.mongo_settings",
        },
        "test_dirs": ["tests"],
    },
    "django-allauth": {
        "apps": {
            "src": os.path.join("settings", "allauth_apps.py"),
            "target": os.path.join("src", "django-allauth", "allauth", "mongo_apps.py"),
        },
        "command": "python",
        "cwd": os.path.join("src", "django-allauth"),
        "project_dir": os.path.join("src", "django-allauth"),
        "settings_file": {
            "test": {
                "src": os.path.join("settings", "allauth_settings.py"),
                "target": os.path.join(
                    "src", "django-allauth", "allauth", "mongo_settings.py"
                ),
            },
            "migrate": {
                "src": os.path.join("settings", "allauth_settings.py"),
                "target": os.path.join(
                    "src", "django-allauth", "allauth", "mongo_settings.py"
                ),
            },
        },
        "settings_module": {
            "test": "allauth.mongo_settings",
            "migrate": "allauth.mongo_settings",
        },
        "migrations_dir": {
            "src": os.path.join("src", "django-mongodb-project", "mongo_migrations"),
            "target": os.path.join(
                "src", "django-allauth", "allauth", "mongo_migrations"
            ),
        },
        "test_dirs": [os.path.join("src", "django-allauth", "tests")],
    },
}
