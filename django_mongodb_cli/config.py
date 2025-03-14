from os.path import join

test_settings_map = {
    "mongo-python-driver": {
        "cmd": "just",
        "cwd": join("src", "mongo-python-driver", "test"),
        "repo": join("src", "mongo-python-driver"),
        "tests": [
            join("src", "mongo-python-driver", "test"),
        ],
    },
    "django": {
        "cmd": "./runtests.py",
        "cwd": join("src", "django", "tests"),
        "repo": join("src", "django"),
        "migrations": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "django", "tests"),
        },
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
        "tests": [
            join("src", "django", "tests"),
            join("src", "django-mongodb-backend", "tests"),
        ],
    },
    "django-filter": {
        "apps": {
            "src": join("settings", "filter_apps.py"),
            "target": join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "cmd": "./runtests.py",
        "cwd": join("src", "django-filter"),
        "migrations": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "django-filter", "tests", "mongo_migrations"),
        },
        "repo": join("src", "django-filter"),
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
        "tests": [join("src", "django-filter", "tests")],
    },
    "django-rest-framework": {
        "apps": {
            "src": join("settings", "rest_framework_apps.py"),
            "target": join("src", "django-rest-framework", "tests", "mongo_apps.py"),
        },
        "migrations": {
            "src": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-rest-framework", "tests", "mongo_migrations"),
        },
        "cmd": "./runtests.py",
        "cwd": join("src", "django-rest-framework"),
        "repo": join("src", "django-rest-framework"),
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
        "tests": [join("src", "django-rest-framework", "tests")],
    },
    "wagtail": {
        "apps": {
            "src": join("settings", "apps_wagtail.py"),
            "target": join("src", "wagtail", "wagtail", "test", "mongo_apps.py"),
        },
        "migrations": {
            "src": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "wagtail", "wagtail", "test", "mongo_migrations"),
        },
        "cmd": "./runtests.py",
        "cwd": join("src", "wagtail"),
        "repo": join("src", "wagtail"),
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
        "tests": [
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
        "cmd": "python",
        "cwd": join("src", "django-debug-toolbar"),
        "repo": join("src", "django-debug-toolbar"),
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
        "tests": ["tests"],
    },
    "django-allauth": {
        "apps": {
            "src": join("settings", "allauth_apps.py"),
            "target": join("src", "django-allauth", "allauth", "mongo_apps.py"),
        },
        "cmd": "python",
        "cwd": join("src", "django-allauth"),
        "repo": join("src", "django-allauth"),
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
        "migrations": {
            "src": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-allauth", "allauth", "mongo_migrations"),
        },
        "tests": [join("src", "django-allauth", "tests")],
    },
}
