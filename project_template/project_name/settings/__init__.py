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
ROOT_URLCONF = "{{ project_name }}.urls"
