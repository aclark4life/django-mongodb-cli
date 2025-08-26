import os

from bson.binary import Binary
from django_mongodb_backend import parse_uri
from pymongo.encryption import AutoEncryptionOpts


KMS_CREDENTIALS = {}

# KMS_CREDENTIALS = {
#     "aws": {
#         "key": os.getenv("AWS_KEY_ARN", ""),
#         "region": os.getenv("AWS_KEY_REGION", ""),
#     },
#     "azure": {
#         "keyName": os.getenv("AZURE_KEY_NAME", ""),
#         "keyVaultEndpoint": os.getenv("AZURE_KEY_VAULT_ENDPOINT", ""),
#     },
#     "gcp": {
#         "projectId": os.getenv("GCP_PROJECT_ID", ""),
#         "location": os.getenv("GCP_LOCATION", ""),
#         "keyRing": os.getenv("GCP_KEY_RING", ""),
#         "keyName": os.getenv("GCP_KEY_NAME", ""),
#     },
#     "kmip": {},
#     "local": {},
# }

KMS_PROVIDERS = {
    # "aws": {},
    # "azure": {},
    # "gcp": {},
    # "kmip": {
    #     "endpoint": os.getenv("KMIP_KMS_ENDPOINT", "not a valid endpoint"),
    # },
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
        from django_mongodb_backend.model_utils import model_has_encrypted_fields

        if model:
            return db == (
                "encrypted" if model_has_encrypted_fields(model) else "default"
            )
        return db == "default"

    def db_for_read(self, model, **hints):
        from django_mongodb_backend.model_utils import model_has_encrypted_fields

        if model_has_encrypted_fields(model):
            return "encrypted"
        return "default"

    db_for_write = db_for_read

    def kms_provider(self, model):
        return "local"


EXPECTED_ENCRYPTED_FIELDS_MAP = {
    "encryption__appointment": {
        "fields": [
            {
                "bsonType": "date",
                "path": "time",
                "keyId": Binary(b"&Y\xea\xe4yhGZ\xb1\xc5R\xe2\x05OY\x15", 4),
                "queries": {"queryType": "equality"},
            }
        ]
    },
    "encryption__billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "keyId": Binary(b"\x8a:r\x1a\x1a\x05Gd\xba\xc1\xc2\xa2z\xce8\x02", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "long",
                "path": "cc_number",
                "keyId": Binary(b"\\N<\x83\xb4\x9aA\xa7\x8b\xc3\xd5Z\x80\xd3\x96@", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "decimal",
                "path": "account_balance",
                "keyId": Binary(b'"z\x9f\x92\xbb\x1c@\xe5\x93+<\x06\x9d\xbe\x93:', 4),
                "queries": {"queryType": "range"},
            },
        ]
    },
    "encryption__patientportaluser": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ip_address",
                "keyId": Binary(b"q\xc8\xfd)\xec\xdcOP\x9d\xb2j\x1b\xd6\xb6<<", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "url",
                "keyId": Binary(b"\xfcN\xeb\xd1N\x8bB\xa4\x8bs\xa3\xafA:\xeax", 4),
                "queries": {"queryType": "equality"},
            },
        ]
    },
    "encryption__patientrecord": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ssn",
                "keyId": Binary(b"\x01\xbca\x08\t\xd6N\\\x81\xbfKg\x97\xb4\xf04", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "date",
                "path": "birth_date",
                "keyId": Binary(b"M\xbc1\x0c\xb8'J7\x9bM\xf0\xb3\xb3\xc9Y\x14", 4),
                "queries": {"queryType": "range"},
            },
            {
                "bsonType": "binData",
                "path": "profile_picture",
                "keyId": Binary(
                    b"\xc1\xc7a\xb9\xe0\x1eGz\xbc\x9c_\x1f[\xd8\xea\xe0", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "patient_age",
                "keyId": Binary(
                    b"V\xa8X\x89\xbd\xd9J\x1f\x8d\x10\xd5\xae\xe7\x13{\xea", 4
                ),
                "queries": {"queryType": "range", "min": 0, "max": 100},
            },
            {
                "bsonType": "double",
                "path": "weight",
                "keyId": Binary(b"L\xf0$\xde\xfd\\Gs\xa2\xed\x0e\xe1Wn#I", 4),
                "queries": {"queryType": "range"},
            },
        ]
    },
    "encryption__patient": {
        "fields": [
            {
                "bsonType": "int",
                "path": "patient_id",
                "keyId": Binary(b"\xa4)\x10\x1fQ\xccH@\x95\xca\xf1]\x83\xed6\xbb", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "patient_name",
                "keyId": Binary(
                    b"\xda\x81\x85\xfb\x16\x8aD;\x83\xae\xd4\xe3_\xda#T", 4
                ),
            },
            {
                "bsonType": "string",
                "path": "patient_notes",
                "keyId": Binary(
                    b"\xc6\xc0\xdb\xb2\xf0\x1cO\x98\x9d\xe7k\xdaACK\x06", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "date",
                "path": "registration_date",
                "keyId": Binary(b"\xc5K\xac\xd9\x04\xacEV\xaaPm\xe8\xdaa&\x9a", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "bool",
                "path": "is_active",
                "keyId": Binary(
                    b"\xfc\xdd\xa0\x1b\xb8\xf9F\xa4\xac\xdfM\x8b\x89\xce\xc3\xdf", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "email",
                "keyId": Binary(b"\x97\xefII\xe9\x9fE\xf8\xae\x8f6\xee.\xd3]K", 4),
                "queries": {"queryType": "equality"},
            },
        ]
    },
    "encryption__encryptednumbers": {
        "fields": [
            {
                "bsonType": "int",
                "path": "pos_bigint",
                "keyId": Binary(b"\x16#3lusB8\x99\xa9q\xec\xa8\x94\x0b\x8b", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "pos_smallint",
                "keyId": Binary(b"H)=\xf4\xccfA\xef\x803(\xbf\x95\xc6jj", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "smallint",
                "keyId": Binary(b"\x8e\xab\x11\x9c\xbbTJc\xbc(\x13+~z\xdc\x1e", 4),
                "queries": {"queryType": "equality"},
            },
        ]
    },
}

DATABASE_ROUTERS = [EncryptedRouter()]
DATABASE_URL = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
KEY_VAULT_NAMESPACE = "keyvault.__keyvault"
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
                kms_providers=KMS_PROVIDERS,
                # encrypted_fields_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
            )
        },
        db_name="encrypted",
    ),
}
DATABASES["encrypted"]["KMS_CREDENTIALS"] = KMS_CREDENTIALS

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
