import django_mongodb
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASES = {"default": django_mongodb.parse_uri(os.environ.get("MONGODB_URI"))}
DEBUG = True
INSTALLED_APPS = [
    "django_extensions",
    "webpack_boilerplate",
]
ROOT_URLCONF = "{{ project_name }}.urls"
