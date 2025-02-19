import os

test_settings_map = {
    "django": {
        "src": os.path.join("settings_test", "settings_django.py"),
        "dest": os.path.join("src", "django", "tests", "mongo_settings.py"),
        "project_dir": os.path.join("src", "django"),
        "command": "./runtests.py",
        "test_dir": os.path.join("src", "django", "tests"),
        "test_dirs": [os.path.join("src", "django", "tests")],
        "settings_module": "mongo_settings",
    },
    "django_filter": {
        "src": os.path.join("settings_test", "settings_filter.py"),
        "dest": os.path.join(
            "src", "django-filter", "django_filters", "mongo_settings.py"
        ),
        "project_dir": os.path.join("src", "django-filter"),
        "command": "./runtests.py",
        "test_dir": os.path.join("src", "django-filter"),
        "test_dirs": [os.path.join("src", "django-filter", "tests")],
        "settings_module": "tests.mongo_settings",
        "apps": {
            "src": os.path.join("apps_test", "apps_filter.py"),
            "dest": os.path.join("src", "django", "tests", "mongo_apps.py"),
        },
    },
    "django_allauth": {
        "src": os.path.join("settings_test", "settings_allauth_regular.py"),
        "dest": "mongo_settings.py",
        "project_dir": os.path.join("src", "django-allauth"),
        "command": "tox",
        "test_dirs": ["tests"],
        "settings_module": "mongo_settings",
    },
    "django_debug_toolbar": {
        "src": os.path.join("settings_test", "settings_debug_toolbar.py"),
        "dest": "mongo_settings.py",
        "project_dir": os.path.join("src", "django-debug-toolbar"),
        "command": "pytest",
        "test_dirs": ["tests"],
        "settings_module": "mongo_settings",
    },
    "django_rest_framework": {
        "src": os.path.join("settings_test", "settings_drf.py"),
        "dest": "conftest.py",
        "project_dir": os.path.join("src", "django-rest-framework"),
        "command": "./runtests.py",
        "test_dirs": ["tests"],
        "settings_module": "mongo_settings",
    },
    "wagtail": {
        "src": os.path.join("settings_test", "settings_wagtail.py"),
        "dest": "mongo_settings.py",
        "project_dir": os.path.join("src", "wagtail"),
        "command": "./runtests.py",
        "test_dirs": ["tests"],
        "settings_module": "mongo_settings",
    },
}
