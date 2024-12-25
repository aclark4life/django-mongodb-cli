import django_mongodb
import os

from secrets import choice
from string import ascii_letters, digits, punctuation

chars = ascii_letters + digits + punctuation

SECRET_KEY = "".join(choice(chars) for _ in range(50))

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {"default": django_mongodb.parse_uri(os.environ.get("MONGODB_URI"))}
DEBUG = True
DEFAULT_AUTO_FIELD = "django_mongodb.fields.ObjectIdAutoField"
INSTALLED_APPS = [
    "{{ project_name }}.mongo_apps.MongoAuthConfig",
    "{{ project_name }}.mongo_apps.MongoContentTypesConfig",
    "django_extensions",
    "webpack_boilerplate",
    "apps.home",
]
MIGRATION_MODULES = {
    "admin": "mongo_migrations.admin",
    "auth": "mongo_migrations.auth",
    "contenttypes": "mongo_migrations.contenttypes",
    "taggit": "mongo_migrations.taggit",
    "wagtaildocs": "mongo_migrations.wagtaildocs",
    "wagtailredirects": "mongo_migrations.wagtailredirects",
    "wagtailimages": "mongo_migrations.wagtailimages",
    "wagtailsearch": "mongo_migrations.wagtailsearch",
    "wagtailadmin": "mongo_migrations.wagtailadmin",
    "wagtailcore": "mongo_migrations.wagtailcore",
    "wagtailforms": "mongo_migrations.wagtailforms",
    "wagtailembeds": "mongo_migrations.wagtailembeds",
    "wagtailusers": "mongo_migrations.wagtailusers",
}
ROOT_URLCONF = "{{ project_name }}.urls"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "frontend", "build")]

WEBPACK_LOADER = {
    "MANIFEST_FILE": os.path.join(BASE_DIR, "frontend", "build", "manifest.json")
}
