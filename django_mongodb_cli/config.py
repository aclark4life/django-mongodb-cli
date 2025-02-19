import os

test_settings_map = {
    "django": {
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django", "tests"),
        "project_dir": os.path.join("src", "django"),
        "settings_module": "mongo_settings",
        "src": os.path.join("settings_test", "settings_django.py"),
        "target": os.path.join("src", "django", "tests", "mongo_settings.py"),
        "test_dirs": [os.path.join("src", "django", "tests")],
    },
    "django_filter": {
        "apps": {
            "src": os.path.join("apps_test", "apps_filter.py"),
            "target": os.path.join("src", "django-filter", "tests", "mongo_apps.py"),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django-filter"),
        "project_dir": os.path.join("src", "django-filter"),
        "settings_module": "tests.settings",
        "src": os.path.join("settings_test", "settings_filter.py"),
        "target": os.path.join("src", "django-filter", "tests", "settings.py"),
        "test_dirs": [os.path.join("src", "django-filter", "tests")],
    },
    "django_rest_framework": {
        "apps": {
            "src": os.path.join("apps_test", "apps_drf.py"),
            "target": os.path.join(
                "src", "django-rest-framework", "tests", "mongo_apps.py"
            ),
        },
        "command": "./runtests.py",
        "cwd": os.path.join("src", "django-rest-framework"),
        "project_dir": os.path.join("src", "django-rest-framework"),
        "settings_module": "mongo_settings",
        "src": os.path.join("settings_test", "settings_drf.py"),
        "target": os.path.join("src", "django-rest-framework", "tests", "conftest.py"),
        "test_dirs": ["tests"],
    },
    "django_allauth": {
        "command": "tox",
        "project_dir": os.path.join("src", "django-allauth"),
        "settings_module": "mongo_settings",
        "src": os.path.join("settings_test", "settings_allauth_regular.py"),
        "target": "mongo_settings.py",
        "test_dirs": ["tests"],
    },
    "django_debug_toolbar": {
        "command": "pytest",
        "project_dir": os.path.join("src", "django-debug-toolbar"),
        "settings_module": "mongo_settings",
        "src": os.path.join("settings_test", "settings_debug_toolbar.py"),
        "target": "mongo_settings.py",
        "test_dirs": ["tests"],
    },
    "wagtail": {
        "command": "./runtests.py",
        "project_dir": os.path.join("src", "wagtail"),
        "settings_module": "mongo_settings",
        "src": os.path.join("settings_test", "settings_wagtail.py"),
        "target": "mongo_settings.py",
        "test_dirs": ["tests"],
    },
}
