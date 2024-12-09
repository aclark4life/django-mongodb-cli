import django_mongodb
import os

DATABASES = {"default": django_mongodb.parse_uri(os.environ.get("MONGODB_URI"))}
