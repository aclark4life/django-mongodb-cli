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
        "apps": {},
        "cmd": "./runtests.py",
        "cwd": join("src", "django", "tests"),
        "repo": join("src", "django"),
        "migrations": {
            "source": join(
                "src",
                "django-mongodb-templates",
                "project_template",
                "mongo_migrations",
            ),
            "target": join("src", "django", "tests"),
        },
        "settings": {
            "test": {
                "source": join("settings", "django_settings.py"),
                "target": join("src", "django", "tests", "mongo_settings.py"),
            },
            "migrate": {
                "source": join("settings", "django_settings.py"),
                "target": join("src", "django", "tests", "mongo_settings.py"),
            },
            "module": {
                "test": "mongo_settings",
                "migrate": "mongo_settings",
            },
        },
        "tests": [
            join("src", "django", "tests"),
            join("src", "django-mongodb-backend", "tests"),
        ],
    },
    "django-filter": {
        "apps": {
            "source": join("settings", "filter_apps.py"),
            "target": join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "cmd": "./runtests.py",
        "cwd": join("src", "django-filter"),
        "migrations": {
            "source": join(
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
                "source": join("settings", "filter_settings.py"),
                "target": join("src", "django-filter", "tests", "settings.py"),
            },
            "migrate": {
                "source": join("settings", "filter_settings.py"),
                "target": join("src", "django-filter", "tests", "settings.py"),
            },
            "module": {
                "test": "tests.settings",
                "migrate": "tests.settings",
            },
        },
        "tests": [join("src", "django-filter", "tests")],
    },
    "django-rest-framework": {
        "apps": {
            "source": join("settings", "rest_framework_apps.py"),
            "target": join("src", "django-rest-framework", "tests", "mongo_apps.py"),
        },
        "migrations": {
            "source": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-rest-framework", "tests", "mongo_migrations"),
        },
        "cmd": "./runtests.py",
        "cwd": join("src", "django-rest-framework"),
        "repo": join("src", "django-rest-framework"),
        "settings_file": {
            "test": {
                "source": join("settings", "rest_framework_settings.py"),
                "target": join("src", "django-rest-framework", "tests", "conftest.py"),
            },
            "migrate": {
                "source": join("settings", "rest_framework_migrate.py"),
                "target": join("src", "django-rest-framework", "tests", "conftest.py"),
            },
            "module": {
                "test": "tests.conftest",
                "migrate": "tests.conftest",
            },
        },
        "tests": [join("src", "django-rest-framework", "tests")],
    },
    "wagtail": {
        "apps": {
            "source": join("settings", "apps_wagtail.py"),
            "target": join("src", "wagtail", "wagtail", "test", "mongo_apps.py"),
        },
        "migrations": {
            "source": join(
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
                "source": join("settings", "settings_wagtail.py"),
                "target": join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
            "migrate": {
                "source": join("settings", "settings_wagtail.py"),
                "target": join(
                    "src", "wagtail", "wagtail", "test", "mongo_settings.py"
                ),
            },
            "module": {
                "test": "wagtail.test.mongo_settings",
                "migrate": "wagtail.test.mongo_settings",
            },
        },
        "tests": [
            join("src", "wagtail", "wagtail", "tests"),
            join("src", "wagtail", "wagtail", "test"),
        ],
    },
    "django-debug-toolbar": {
        "apps": {
            "source": join("settings", "debug_toolbar_apps.py"),
            "target": join(
                "src", "django-debug-toolbar", "debug_toolbar", "mongo_apps.py"
            ),
        },
        "cmd": "python",
        "cwd": join("src", "django-debug-toolbar"),
        "repo": join("src", "django-debug-toolbar"),
        "settings_file": {
            "test": {
                "source": join("settings", "debug_toolbar_settings.py"),
                "target": join(
                    "src", "django-debug-toolbar", "debug_toolbar", "mongo_settings.py"
                ),
            },
            "migrate": {
                "source": join("settings", "debug_toolbar_settings.py"),
                "target": join(
                    "src", "django-debug-toolbar", "debug_toolbar", "mongo_settings.py"
                ),
            },
            "module": {
                "test": "debug_toolbar.mongo_settings",
                "migrate": "debug_toolbar.mongo_settings",
            },
        },
        "tests": [
            join("src", "django-debug-toolbar", "tests"),
        ],
    },
    "django-allauth": {
        "cmd": "pytest",
        "cwd": join("src", "django-allauth"),
        "repo": join("src", "django-allauth"),
        "apps": {
            "source": join("settings", "allauth_apps.py"),
            "target": join("src", "django-allauth", "allauth", "mongo_apps.py"),
        },
        "settings_file": {
            "test": {
                "source": join("settings", "allauth_settings.py"),
                "target": join("src", "django-allauth", "allauth", "mongo_settings.py"),
            },
            "migrate": {
                "source": join("settings", "allauth_settings.py"),
                "target": join("src", "django-allauth", "allauth", "mongo_settings.py"),
            },
            "module": {
                "test": "allauth.mongo_settings",
                "migrate": "allauth.mongo_settings",
            },
        },
        "migrations": {
            "source": join("src", "django-mongodb-project", "mongo_migrations"),
            "target": join("src", "django-allauth", "allauth", "mongo_migrations"),
        },
        "tests": [
            join("src", "django-allauth", "allauth", "usersessions", "tests"),
            join("src", "django-allauth", "allauth", "core", "tests"),
            join("src", "django-allauth", "allauth", "core", "internal", "tests"),
            join("src", "django-allauth", "allauth", "tests"),
            join("src", "django-allauth", "allauth", "mfa", "recovery_codes", "tests"),
            join("src", "django-allauth", "allauth", "mfa", "webauthn", "tests"),
            join("src", "django-allauth", "allauth", "mfa", "totp", "tests"),
            join("src", "django-allauth", "allauth", "mfa", "base", "tests"),
            join(
                "src",
                "django-allauth",
                "allauth",
                "socialaccount",
                "providers",
                "oauth2",
                "tests",
            ),
            join("src", "django-allauth", "allauth", "socialaccount", "tests"),
            join(
                "src", "django-allauth", "allauth", "socialaccount", "internal", "tests"
            ),
            join("src", "django-allauth", "allauth", "templates", "tests"),
            join(
                "src", "django-allauth", "allauth", "headless", "usersessions", "tests"
            ),
            join("src", "django-allauth", "allauth", "headless", "tests"),
            join("src", "django-allauth", "allauth", "headless", "spec", "tests"),
            join("src", "django-allauth", "allauth", "headless", "internal", "tests"),
            join("src", "django-allauth", "allauth", "headless", "mfa", "tests"),
            join(
                "src", "django-allauth", "allauth", "headless", "socialaccount", "tests"
            ),
            join(
                "src",
                "django-allauth",
                "allauth",
                "headless",
                "contrib",
                "ninja",
                "tests",
            ),
            join(
                "src",
                "django-allauth",
                "allauth",
                "headless",
                "contrib",
                "rest_framework",
                "tests",
            ),
            join("src", "django-allauth", "allauth", "headless", "account", "tests"),
            join("src", "django-allauth", "allauth", "headless", "base", "tests"),
            join("src", "django-allauth", "allauth", "account", "tests"),
            join("src", "django-allauth", "tests"),
        ],
    },
}
