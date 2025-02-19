import os

import django_mongodb_backend

DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/djangotests")

MIGRATION_MODULES = {
    "admin": "tests.mongo_migrations.admin",
    "auth": "tests.mongo_migrations.auth",
    "contenttypes": "tests.mongo_migrations.contenttypes",
}


DEBUG_PROPAGATE_EXCEPTIONS = (True,)
# DATABASES={
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:'
#     },
#     'secondary': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:'
#     }
# },
DATABASES = (
    {
        "default": django_mongodb_backend.parse_uri(DATABASE_URL),
    },
)
SITE_ID = (1,)
SECRET_KEY = ("not very secret in tests",)
USE_I18N = (True,)
STATIC_URL = ("/static/",)
ROOT_URLCONF = ("tests.urls",)
TEMPLATES = (
    [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "debug": True,  # We want template errors to raise
            },
        },
    ],
)
MIDDLEWARE = (
    (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ),
)
INSTALLED_APPS = (
    (
        "tests.mongo_apps.MongoAdminConfig",
        "tests.mongo_apps.MongoAuthConfig",
        "tests.mongo_apps.MongoContentTypesConfig",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "tests.authentication",
        "tests.generic_relations",
        "tests.importable",
        "tests",
    ),
)
PASSWORD_HASHERS = (("django.contrib.auth.hashers.MD5PasswordHasher",),)
DEFAULT_AUTO_FIELD = ("django_mongodb_backend.fields.ObjectIdAutoField",)
MIGRATION_MODULES = (
    {
        "admin": "tests.mongo_migrations.admin",
        "auth": "tests.mongo_migrations.auth",
        "contenttypes": "tests.mongo_migrations.contenttypes",
        "tests": "tests.mongo_migrations.tests",
    },
)
