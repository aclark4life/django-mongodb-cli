import django_mongodb
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASES = {"default": django_mongodb.parse_uri(os.environ.get("MONGODB_URI"))}
DEBUG = True
DEFAULT_AUTO_FIELD = "django_mongodb.fields.ObjectIdAutoField"
INSTALLED_APPS = [
    "{{ project_name }}.mongo_apps.MongoAuthConfig",
    "django.contrib.contenttypes",
    "django_extensions",
    "webpack_boilerplate",
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
