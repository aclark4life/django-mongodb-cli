import os


test_settings_map = {
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
