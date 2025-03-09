from os.path import join

test_settings_map = {
    "django": {
        "cwd": join("src", "django", "tests"),
        "command": "./runtests.py",
        "migrations_dir": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "django", "tests"),
        },
        "project_dir": join("src", "django"),
        "settings_file": {
            "test": {
                "src": join("settings", "django_settings.py"),
                "target": join("src", "django", "tests", "mongo_settings.py"),
            },
            "migrate": {
                "src": join("settings", "django_settings.py"),
                "target": join("src", "django", "tests", "mongo_settings.py"),
            },
        },
        "settings_module": {
            "test": "mongo_settings",
            "migrate": "mongo_settings",
        },
        "target": join("src", "django", "tests", "mongo_settings.py"),
        "test_dirs": [
            join("src", "django", "tests"),
            join("src", "django-mongodb-backend", "tests"),
        ],
    },
    "django-filter": {
        "apps": {
            "src": join("settings", "filter_apps.py"),
            "target": join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "command": "./runtests.py",
        "cwd": join("src", "django-filter"),
        "migrations_dir": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "django-filter", "tests", "mongo_migrations"),
        },
        "project_dir": join("src", "django-filter"),
        "settings_file": {
            "test": {
                "src": join("settings", "filter_settings.py"),
                "target": join("src", "django-filter", "tests", "settings.py"),
            },
            "migrate": {
                "src": join("settings", "filter_settings.py"),
                "target": join("src", "django-filter", "tests", "settings.py"),
            },
        },
        "settings_module": {
            "test": "tests.settings",
            "migrate": "tests.settings",
        },
        "test_dirs": [join("src", "django-filter", "tests")],
    },
    "django-rest-framework": {
        "apps": {
            "src": join("settings", "rest_framework_apps.py"),
            "target": join("src", "django-rest-framework", "tests", "mongo_apps.py"),
        },
        "migrations_dir": {
            "src": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-rest-framework", "tests", "mongo_migrations"),
        },
        "command": "./runtests.py",
        "cwd": join("src", "django-rest-framework"),
        "project_dir": join("src", "django-rest-framework"),
        "settings_file": {
            "test": {
                "src": join("settings", "rest_framework_settings.py"),
                "target": join("src", "django-rest-framework", "tests", "conftest.py"),
            },
            "migrate": {
                "src": join("settings", "rest_framework_migrate.py"),
                "target": join("src", "django-rest-framework", "tests", "conftest.py"),
            },
        },
        "settings_module": {
            "test": "tests.conftest",
            "migrate": "tests.conftest",
        },
        "test_dirs": [join("src", "django-rest-framework", "tests")],
    },
    "wagtail": {
        "apps": {
            "src": join("settings", "apps_wagtail.py"),
            "target": join("src", "wagtail", "wagtail", "test", "mongo_apps.py"),
        },
        "migrations_dir": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "wagtail", "wagtail", "test", "mongo_migrations"),
        },
        "command": "./runtests.py",
        "cwd": join("src", "wagtail"),
        "project_dir": join("src", "wagtail"),
        "settings_file": {
            "test": {
                "src": join("settings", "settings_wagtail.py"),
                "target": join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
            "migrate": {
                "src": join("settings", "settings_wagtail.py"),
                "target": join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
        },
        "settings_module": {
            "test": "wagtail.test.mongo_settings",
            "migrate": "wagtail.test.mongo_settings",
        },
        "test_dirs": [
            join("src", "wagtail", "wagtail", "tests"),
            join("src", "wagtail", "wagtail", "test"),
        ],
    },
    "django-debug-toolbar": {
        "apps": {
            "src": join("settings", "debug_toolbar_apps.py"),
            "target": join(
                "src", "django-debug-toolbar", "debug_toolbar", "mongo_apps.py"
            ),
        },
        "command": "python",
        "cwd": join("src", "django-debug-toolbar"),
        "project_dir": join("src", "django-debug-toolbar"),
        "settings_file": {
            "test": {
                "src": join("settings", "debug_toolbar_settings.py"),
                "target": join(
                    "src", "django-debug-toolbar", "debug_toolbar", "mongo_settings.py"
                ),
            },
            "migrate": {
                "src": join("settings", "debug_toolbar_settings.py"),
                "target": join(
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
            "src": join("settings", "allauth_apps.py"),
            "target": join("src", "django-allauth", "allauth", "mongo_apps.py"),
        },
        "command": "python",
        "cwd": join("src", "django-allauth"),
        "project_dir": join("src", "django-allauth"),
        "settings_file": {
            "test": {
                "src": join("settings", "allauth_settings.py"),
                "target": join("src", "django-allauth", "allauth", "mongo_settings.py"),
            },
            "migrate": {
                "src": join("settings", "allauth_settings.py"),
                "target": join("src", "django-allauth", "allauth", "mongo_settings.py"),
            },
        },
        "settings_module": {
            "test": "allauth.mongo_settings",
            "migrate": "allauth.mongo_settings",
        },
        "migrations_dir": {
            "src": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-allauth", "allauth", "mongo_migrations"),
        },
        "test_dirs": [join("src", "django-allauth", "tests")],
    },
}
