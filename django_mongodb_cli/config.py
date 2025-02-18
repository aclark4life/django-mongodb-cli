import os

test_settings_map = {
    "django": {
        "src": os.path.join("test_settings", "settings_django.py"),
        "dest": os.path.join("src", "django", "mongo_settings.py"),
        "module": "mongo_settings",
        "project_dir": os.path.join("src", "django"),
        "command": "./runtests.py",
        "test_dirs": [os.path.join("src", "django", "tests")],
    },
    "django_allauth": {
        "src": os.path.join("test_settings", "settings_allauth_regular.py"),
        "dest": "mongo_settings.py",
        "module": "allauth.mongo_settings",
        "project_dir": os.path.join("src", "django-allauth"),
        "command": "tox",
        "test_dirs": ["tests"],
    },
    "django_debug_toolbar": {
        "src": os.path.join("test_settings", "settings_debug_toolbar.py"),
        "dest": "mongo_settings.py",
        "module": "debug_toolbar.mongo_settings",
        "project_dir": os.path.join("src", "django-debug-toolbar"),
        "command": "pytest",
        "test_dirs": ["tests"],
    },
    "django_filter": {
        "src": os.path.join("test_settings", "settings_filter.py"),
        "dest": "mongo_settings.py",
        "module": "django_filters.mongo_settings",
        "project_dir": os.path.join("src", "django-filter"),
        "command": "./runtests.py",
        "test_dirs": [os.path.join("src", "django-filter")],
    },
    "django_rest_framework": {
        "src": os.path.join("test_settings", "settings_drf.py"),
        "dest": "conftest.py",
        "module": "rest_framework.mongo_settings",
        "project_dir": os.path.join("src", "django-rest-framework"),
        "command": "./runtests.py",
        "test_dirs": ["tests"],
    },
    "wagtail": {
        "src": os.path.join("test_settings", "settings_wagtail.py"),
        "dest": "mongo_settings.py",
        "module": "wagtail.test.mongo_settings",
        "project_dir": os.path.join("src", "wagtail"),
        "command": "./runtests.py",
        "test_dirs": ["tests"],
    },
}
