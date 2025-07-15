import os

from django_mongodb_backend import encryption, parse_uri
from pymongo.encryption import AutoEncryptionOpts

schema_map = {
    "fields": [
        {
            "bsonType": "string",
            "path": "ssn",
            "queries": {"queryType": "equality", "contention": 1},
        },
        {"bsonType": "int", "path": "patient_id"},
        {"bsonType": "string", "path": "patient_name"},
    ]
}


DATABASE_ROUTERS = [encryption.EncryptedRouter()]
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DATABASES = {
    "default": parse_uri(
        DATABASE_URL,
        db_name="test",
    ),
    "encrypted": parse_uri(
        DATABASE_URL,
        options={
            "auto_encryption_opts": AutoEncryptionOpts(
                key_vault_namespace=encryption.KEY_VAULT_NAMESPACE,
                kms_providers=encryption.KMS_PROVIDERS,
                schema_map=schema_map,
            )
        },
        db_name="encrypted",
    ),
}
DATABASES["encrypted"]["KMS_PROVIDERS"] = encryption.KMS_PROVIDERS

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
