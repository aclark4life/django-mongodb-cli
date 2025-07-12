import os

from django_mongodb_backend import encryption, parse_uri

KMS_PROVIDER = "local"

AUTO_ENCRYPTION_OPTS = encryption.get_auto_encryption_opts(
    key_vault_namespace=encryption.KEY_VAULT_NAMESPACE,
    kms_providers=encryption.KMS_PROVIDERS,
)

DATABASE_ROUTERS = [encryption.EncryptedRouter()]
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DATABASES = {
    "default": parse_uri(
        DATABASE_URL,
        db_name="test",
    ),
    "encrypted": parse_uri(
        DATABASE_URL,
        options={"auto_encryption_opts": AUTO_ENCRYPTION_OPTS},
        db_name="encrypted",
    ),
}

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
