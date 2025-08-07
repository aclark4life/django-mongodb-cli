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
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xc7K\xd8\x0b0>H]\x9d\xc2)\x07l\x07\x86;", 4),
            }
        ]
    },
    "encryption__billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x14\x08\xe7\xa92\xdeO\x01\xa4\x17(\x16p\xfb\xc6i", 4
                ),
            },
            {
                "bsonType": "long",
                "path": "cc_number",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\x06FY\xfd7-Br\xaa7A[\xf0/\x0b=", 4),
            },
            {
                "bsonType": "decimal",
                "path": "account_balance",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"o\xc2]:\x83\x9eO\x1e\xb1?\x19\x17\xfa=ah", 4),
            },
        ]
    },
    "encryption__patientportaluser": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ip_address",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"^\x99\xde\\rHF\x94\x90\x90\x97)/2b#", 4),
            },
            {
                "bsonType": "string",
                "path": "url",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\xabs\x1b\xe5\x12\x89H\x93\xa9\xc56\x02\x10\xfbsv", 4
                ),
            },
        ]
    },
    "encryption__patientrecord": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ssn",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x08}\x99S\xc5\xa6F\xb9\xad\x02\xd1\xbe\xd9\x8a\xcb\xb0", 4
                ),
            },
            {
                "bsonType": "date",
                "path": "birth_date",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"g\x8e)\x89T\x9fHm\xa1\x95\x9d\xac\x93\t\x8b\xbc", 4),
            },
            {
                "bsonType": "binData",
                "path": "profile_picture",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"u\x13\xfe\xff\xeb\x9dM9\x8b\xbe\xaa\x7f*DW{", 4),
            },
            {
                "bsonType": "int",
                "path": "patient_age",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\xa5b\xb1S\xb0\xd2A\xf8\xbc3c@\xba\x9dAA", 4),
            },
            {
                "bsonType": "double",
                "path": "weight",
                "queries": {"queryType": "range"},
                "keyId": Binary(
                    b"\x9fi`\xcf\xbc!L\x80\x84\x14\xe9\\\xcd\x04\xef\xd9", 4
                ),
            },
        ]
    },
    "encryption__patient": {
        "fields": [
            {
                "bsonType": "int",
                "path": "patient_id",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xfe\xbf\xe9*+0E!\x88\x13~\x8c\xfbk:\xc0", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_name",
                "keyId": Binary(b"3HV\xf0q\xbaAQ\x9d\xf8\xeb[\x03\xcb\xbf\x8b", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_notes",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xe0}\x96\x1cH\\I\xf8\xa3\rA\x04\x8bNpI", 4),
            },
            {
                "bsonType": "date",
                "path": "registration_date",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xc5\xee\xabW\xa0JN|\x90\x90\xb9\xca\x193v\xd5", 4),
            },
            {
                "bsonType": "bool",
                "path": "is_active",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\xce\xee\x9d_\x97_@Z\x85\xf4\xf0 \x18\xf4\xa6\xf8", 4
                ),
            },
            {
                "bsonType": "string",
                "path": "email",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"q5J/{\xdfJ\xf5\xb6?h\xf0M@\x8c\xba", 4),
            },
        ]
    },
    "encryption__encryptednumbers": {
        "fields": [
            {
                "bsonType": "int",
                "path": "pos_bigint",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"9\xdf\xc4u\xa0yO\xda\x8c%h\x92\xda\xf0\xd6\x0f", 4),
            },
            {
                "bsonType": "int",
                "path": "pos_smallint",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"h\x02O-DYGh\x99\x15\xdfd\xc4\x9aL\x97", 4),
            },
            {
                "bsonType": "int",
                "path": "smallint",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"K)\xe2\xd6\xadUDf\xbdu\xb7-n\x934\xfa", 4),
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
    "encrypted": parse_uri(
        DATABASE_URL,
        options={
            "auto_encryption_opts": AutoEncryptionOpts(
                key_vault_namespace=KEY_VAULT_NAMESPACE,
                kms_providers=KMS_PROVIDERS,
                # encrypted_fields_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
                encrypted_fields_map={},
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
