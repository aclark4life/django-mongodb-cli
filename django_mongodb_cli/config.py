import os

test_settings_map = {
    "default": {
        "src": "settings_django.py",
        "dest": "mongo_settings.py",
        "module": "mongo_settings",
        "path": os.path.join("src", "django", "tests"),
    },
    "django_allauth": {
        "src": "settings_allauth_regular.py",
        "dest": "mongo_settings.py",
        "module": "allauth.mongo_settings",
        "path": os.path.join("src", "django-allauth"),
    },
    "django_debug_toolbar": {
        "src": "settings_debug_toolbar.py",
        "dest": "mongo_settings.py",
        "module": "debug_toolbar.mongo_settings",
        "path": os.path.join("src", "django-debug-toolbar"),
    },
    "django_filter": {
        "src": "settings_filter.py",
        "dest": "mongo_settings.py",
        "module": "django_filters.mongo_settings",
        "path": os.path.join("src", "django-filter"),
    },
    "django_rest_framework": {
        "src": "settings_drf.py",
        "dest": "conftest.py",
        "module": "rest_framework.mongo_settings",
        "path": os.path.join("src", "django-rest-framework"),
    },
    "wagtail": {
        "src": "settings_wagtail.py",
        "dest": "mongo_settings.py",
        "module": "wagtail.test.mongo_settings",
        "path": os.path.join("src", "wagtail"),
    },
}


run_tests_map = {
    "default": "./runtests.py",
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
