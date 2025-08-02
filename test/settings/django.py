import os

from bson.binary import Binary
from django_mongodb_backend import parse_uri
from pymongo.encryption import AutoEncryptionOpts

from django_mongodb_backend.fields import has_encrypted_fields


KMS_CREDENTIALS = {
    "aws": {
        "key": os.getenv("AWS_KEY_ARN", ""),
        "region": os.getenv("AWS_KEY_REGION", ""),
    },
    "azure": {
        "keyName": os.getenv("AZURE_KEY_NAME", ""),
        "keyVaultEndpoint": os.getenv("AZURE_KEY_VAULT_ENDPOINT", ""),
    },
    "gcp": {
        "projectId": os.getenv("GCP_PROJECT_ID", ""),
        "location": os.getenv("GCP_LOCATION", ""),
        "keyRing": os.getenv("GCP_KEY_RING", ""),
        "keyName": os.getenv("GCP_KEY_NAME", ""),
    },
    "kmip": {},
    "local": {},
}

KMS_PROVIDERS = {
    "aws": {},
    "azure": {},
    "gcp": {},
    "kmip": {
        "endpoint": os.getenv("KMIP_KMS_ENDPOINT", "not a valid endpoint"),
    },
    "local": {
        "key": bytes.fromhex(
            "000102030405060708090a0b0c0d0e0f"
            "101112131415161718191a1b1c1d1e1f"
            "202122232425262728292a2b2c2d2e2f"
            "303132333435363738393a3b3c3d3e3f"
            "404142434445464748494a4b4c4d4e4f"
            "505152535455565758595a5b5c5d5e5f"
        )
    },
}


class EncryptedRouter:
    def allow_migrate(self, db, app_label, model_name=None, model=None, **hints):
        if model:
            return db == ("other" if has_encrypted_fields(model) else "default")
        return db == "default"

    def db_for_read(self, model, **hints):
        if has_encrypted_fields(model):
            return "other"
        return "default"

    db_for_write = db_for_read

    def kms_provider(self, model):
        return "local"


EXPECTED_ENCRYPTED_FIELDS_MAP = {
    "billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b" \x901\x89\x1f\xafAX\x9b*\xb1\xc7\xc5\xfdl\xa4", 4),
            },
            {
                "bsonType": "long",
                "path": "cc_number",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x97\xb4\x9d\xb8\xd5\xa6Ay\x85\xfe\x00\xc0\xd4{\xa2\xff", 4
                ),
            },
            {
                "bsonType": "decimal",
                "path": "account_balance",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\xcc\x01-s\xea\xd9B\x8d\x80\xd7\xf8!n\xc6\xf5U", 4),
            },
        ]
    },
    "patientrecord": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ssn",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x14F\x89\xde\x8d\x04K7\xa9\x9a\xaf_\xca\x8a\xfb&", 4
                ),
            },
            {
                "bsonType": "date",
                "path": "birth_date",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"@\xdd\xb4\xd2%\xc2B\x94\xb5\x07\xbc(ER[s", 4),
            },
            {
                "bsonType": "binData",
                "path": "profile_picture",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"Q\xa2\xebc!\xecD,\x8b\xe4$\xb6ul9\x9a", 4),
            },
            {
                "bsonType": "int",
                "path": "patient_age",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\ro\x80\x1e\x8e1K\xde\xbc_\xc3bi\x95\xa6j", 4),
            },
            {
                "bsonType": "double",
                "path": "weight",
                "queries": {"queryType": "range"},
                "keyId": Binary(
                    b"\x9b\xfd:n\xe1\xd0N\xdd\xb3\xe7e)\x06\xea\x8a\x1d", 4
                ),
            },
        ]
    },
    "patient": {
        "fields": [
            {
                "bsonType": "int",
                "path": "patient_id",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\x8ft\x16:\x8a\x91D\xc7\x8a\xdf\xe5O\n[\xfd\\", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_name",
                "keyId": Binary(
                    b"<\x9b\xba\xeb:\xa4@m\x93\x0e\x0c\xcaN\x03\xfb\x05", 4
                ),
            },
            {
                "bsonType": "string",
                "path": "patient_notes",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\x01\xe7\xd1isnB$\xa9(gwO\xca\x10\xbd", 4),
            },
            {
                "bsonType": "date",
                "path": "registration_date",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"F\xfb\xae\x82\xd5\x9a@\xee\xbfJ\xaf#\x9c:-I", 4),
            },
            {
                "bsonType": "bool",
                "path": "is_active",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xb2\xb5\xc4K53A\xda\xb9V\xa6\xa9\x97\x94\xea;", 4),
            },
        ]
    },
}
DATABASE_ROUTERS = [EncryptedRouter()]
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
KEY_VAULT_NAMESPACE = "encrypted.__keyvault"
DATABASES = {
    "default": parse_uri(
        DATABASE_URL,
        db_name="test",
    ),
    "other": parse_uri(
        DATABASE_URL,
        options={
            "auto_encryption_opts": AutoEncryptionOpts(
                key_vault_namespace=KEY_VAULT_NAMESPACE,
                kms_providers=KMS_PROVIDERS,
                # schema_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
            )
        },
        db_name="other",
    ),
}
DATABASES["other"]["KMS_CREDENTIALS"] = KMS_CREDENTIALS

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
