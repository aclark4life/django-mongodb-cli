import django_mongodb_backend
import os


DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "NAME": "djangotests",
    },
    "other": {
        "ENGINE": "django_mongodb_backend",
        "NAME": "djangotests-other",
    },
}
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/djangotests")
DATABASES["default"] = django_mongodb_backend.parse_uri(DATABASE_URL)
