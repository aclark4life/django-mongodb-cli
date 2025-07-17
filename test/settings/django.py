import os

from django_mongodb_backend import encryption, parse_uri
from pymongo.encryption import AutoEncryptionOpts

SCHEMA_MAP = {
    "encryption__billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "cc_number",
                "queries": {"queryType": "equality"},
            },
        ]
    },
    "encryption__patientrecord": {
        "fields": [
            {"bsonType": "string", "path": "ssn", "queries": {"queryType": "equality"}}
        ]
    },
    "encryption__patient": {
        "fields": [
            {"bsonType": "int", "path": "patient_id"},
            {
                "bsonType": "int",
                "path": "patient_age",
                "queries": {"queryType": "range"},
            },
            {"bsonType": "string", "path": "patient_name"},
        ]
    },
    "encryption__post": {"fields": [{"bsonType": "string", "path": "title"}]},
    "encryption__integermodel": {"fields": [{"bsonType": "int", "path": "value"}]},
}


DATABASE_ROUTERS = [encryption.EncryptedRouter()]
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
KEY_VAULT_NAMESPACE = "encrypted.__keyvault"
DATABASES = {
    "default": parse_uri(
        DATABASE_URL,
        db_name="test",
    ),
    "encrypted": parse_uri(
        DATABASE_URL,
        options={
            "auto_encryption_opts": AutoEncryptionOpts(
                key_vault_namespace=KEY_VAULT_NAMESPACE,
                kms_providers=encryption.KMS_PROVIDERS,
                schema_map=SCHEMA_MAP,
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
