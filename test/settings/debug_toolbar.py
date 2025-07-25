"""Django settings for tests."""

import os
import django_mongodb_backend

DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/djangotests")
DATABASES = {"default": django_mongodb_backend.parse_uri(DATABASE_URL)}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

SECRET_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

INTERNAL_IPS = ["127.0.0.1"]

LOGGING = {  # avoids spurious output in tests
    "version": 1,
    "disable_existing_loggers": True,
}


# Application definition

INSTALLED_APPS = [
    "debug_toolbar.mongo_apps.MongoAdminConfig",
    "debug_toolbar.mongo_apps.MongoAuthConfig",
    "debug_toolbar.mongo_apps.MongoContentTypesConfig",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "tests",
]


USE_GIS = os.getenv("DB_BACKEND") == "postgis"

if USE_GIS:
    INSTALLED_APPS = ["django.contrib.gis"] + INSTALLED_APPS

MEDIA_URL = "/media/"  # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE = [
    "tests.middleware.UseCacheAfterToolbar",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "NAME": "jinja2",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "DIRS": [os.path.join(BASE_DIR, "tests", "templates", "jinja2")],
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "tests", "static")

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tests", "additional_static"),
    ("prefix", os.path.join(BASE_DIR, "tests", "additional_static")),
]

# Cache and database

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "second": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

# Debug Toolbar configuration

DEBUG_TOOLBAR_CONFIG = {
    # Django's test client sets wsgi.multiprocess to True inappropriately
    "RENDER_PANELS": False,
    # IS_RUNNING_TESTS must be False even though we're running tests because we're running the toolbar's own tests.
    "IS_RUNNING_TESTS": False,
}
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
MIGRATION_MODULES = {
    "admin": None,
    "auth": None,
    "contenttypes": None,
}
