import django_mongodb
import os


DATABASES = {
    "default": {
        "ENGINE": "django_mongodb",
        "NAME": "djangotests",
    },
    "other": {
        "ENGINE": "django_mongodb",
        "NAME": "djangotests-other",
    },
}
DEFAULT_AUTO_FIELD = "django_mongodb.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27017/djangotests")
DATABASES["default"] = django_mongodb.parse_uri(DATABASE_URL)
