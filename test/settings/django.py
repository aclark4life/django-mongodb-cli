import os

from bson.binary import Binary
from django_mongodb_backend import parse_uri
from pymongo.encryption import AutoEncryptionOpts

from django_mongodb_backend.model_utils import model_has_encrypted_fields


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
        if model:
            return db == (
                "encrypted" if model_has_encrypted_fields(model) else "default"
            )
        return db == "default"

    def db_for_read(self, model, **hints):
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
                "keyId": Binary(
                    b"\xbd\xa6\x81\xa0\xea\xf0G\xd5\x87x\x15\xd6\xd0^\xed\xa7", 4
                ),
                "queries": {"queryType": "equality"},
            }
        ]
    },
    "encryption__billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "keyId": Binary(b"d=v\xef\xa3]@g\xac2\xe4\x1a3s\x94\xe0", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "long",
                "path": "cc_number",
                "keyId": Binary(
                    b"l\x1b\x99C\x1e\x8dE\xf8\xaf\xfe9\xbc\xf1\xda\t\x0c", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "decimal",
                "path": "account_balance",
                "keyId": Binary(b"\xb3,\x05\xf5\x92'J\x17\x8a@?V\x82\x07c\x1d", 4),
                "queries": {"queryType": "range"},
            },
        ]
    },
    "encryption__patientportaluser": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ip_address",
                "keyId": Binary(
                    b"\x18\xdc#\xe7f\xccC\xc7\x8d\xbb\xc1\x94\x08\x1b@\x19", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "url",
                "keyId": Binary(
                    b"\re\x1a\xc1x\x11F\xa5\x8d\x8f\x1a\xc8\xaa\x7f\xa4'", 4
                ),
                "queries": {"queryType": "equality"},
            },
        ]
    },
    "encryption__patientrecord": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ssn",
                "keyId": Binary(
                    b"(\x18\x8b\x9e\x8e\x03A\xa2\xa40\x99\xd6\xae\x10\x1eT", 4
                ),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "date",
                "path": "birth_date",
                "keyId": Binary(b"\xaa\xbd3#\x9f+N\x82\x8dZ^j\xb1\x1a\x0e\x1b", 4),
                "queries": {"queryType": "range"},
            },
            {
                "bsonType": "binData",
                "path": "profile_picture",
                "keyId": Binary(b"\xb5N\x17\xafr\xc9It\x80\xb4\x88o\x92\xf57\x02", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "patient_age",
                "keyId": Binary(b"\xc7PWm9\x93L\x89\xbe'\xe8ti\xf1\xb5\xcc", 4),
                "queries": {"queryType": "range", "min": 0, "max": 100},
            },
            {
                "bsonType": "double",
                "path": "weight",
                "keyId": Binary(b"1\xed\x057\xaa\x8bI\x8d\xb4\tV=\x8e\x96\xcd\xf8", 4),
                "queries": {"queryType": "range"},
            },
        ]
    },
    "encryption__patient": {
        "fields": [
            {
                "bsonType": "int",
                "path": "patient_id",
                "keyId": Binary(b")\xe6\xb0i{ZE<\xb1Q\xff]\xf4\x06A\x80", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "patient_name",
                "keyId": Binary(b"~Z\xa7\xe0\x7f/Jz\xa5\xf6vI\xeb\xd6,(", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_notes",
                "keyId": Binary(b"\xcd\x86DFXm@\xe3\x94\x8d\xb3\x80\x9b\xe5\xfaO", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "date",
                "path": "registration_date",
                "keyId": Binary(b"\x0e\x82\xc0\xfeJHK\x0e\xac\xfd\x83Nd\x90\xce\r", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "bool",
                "path": "is_active",
                "keyId": Binary(b"\x97\xc0UHV/B\xd9\x8e0T\xd9\x93a\xcb\x8d", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "string",
                "path": "email",
                "keyId": Binary(b"0\xa7\x03[\xa3pD\x03\x82Iy\xa5\x19\x86\x01\xbc", 4),
                "queries": {"queryType": "equality"},
            },
        ]
    },
    "encryption__encryptednumbers": {
        "fields": [
            {
                "bsonType": "int",
                "path": "pos_bigint",
                "keyId": Binary(b"\x1e\xcapB\xce\xa4OS\x90:@\x93?\xa6\x9d\xcc", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "pos_smallint",
                "keyId": Binary(b"\xeb\xbdo\xb7\xafUHH\xac\x12\n\x8c:v\xc6e", 4),
                "queries": {"queryType": "equality"},
            },
            {
                "bsonType": "int",
                "path": "smallint",
                "keyId": Binary(
                    b"\xd6\x02\xc6\x00\xfd\xadIy\x8d&\xa2M\xde~\x95\xb1", 4
                ),
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
                encrypted_fields_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
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
