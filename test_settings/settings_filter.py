# ensure package/conf is importable
from django_filters.conf import DEFAULTS

import django_mongodb
import os

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": ":memory:",
#     },
# }

DATABASES = {}
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/djangotests")
DATABASES["default"] = django_mongodb.parse_uri(DATABASE_URL)

INSTALLED_APPS = (
    "tests.mongo_apps.MongoContentTypesConfig",
    "django.contrib.staticfiles",
    "tests.mongo_apps.MongoAuthConfig",
    "rest_framework",
    "django_filters",
    "tests.rest_framework",
    "tests",
)

MIDDLEWARE = []

ROOT_URLCONF = "tests.urls"

USE_TZ = True

TIME_ZONE = "UTC"

SECRET_KEY = "foobar"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]


STATIC_URL = "/static/"


# XMLTestRunner output
TEST_OUTPUT_DIR = ".xmlcoverage"


# help verify that DEFAULTS is importable from conf.
def FILTERS_VERBOSE_LOOKUPS():
    return DEFAULTS["VERBOSE_LOOKUPS"]


# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_AUTO_FIELD = "django_mongodb.fields.ObjectIdAutoField"
MIGRATION_MODULES = {
    "admin": "tests.mongo_migrations.admin",
    "auth": "tests.mongo_migrations.auth",
    "contenttypes": "tests.mongo_migrations.contenttypes",
}
