import os

from django_mongodb_backend import encryption, parse_uri
from pymongo.encryption import AutoEncryptionOpts
from bson.binary import Binary

EXPECTED_ENCRYPTED_FIELDS_MAP = {
    "test_encrypted.billing": {
        "fields": [
            {
                "bsonType": "string",
                "path": "cc_type",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"u\x0fk\x9ay\xbcFY\xbf\xc0Oc0?\xbf~", 4),
            },
            {
                "bsonType": "long",
                "path": "cc_number",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"g(\x8b\x8er\xf4O\xcd\x8e\xd2\x0c\x8a\xf9\x94RA", 4),
            },
            {
                "bsonType": "decimal",
                "path": "account_balance",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\xd5\x8e.m8\x18J\xd5\xb0B~c\x11\x07k\xbc", 4),
            },
        ]
    },
    "test_encrypted.patientrecord": {
        "fields": [
            {
                "bsonType": "string",
                "path": "ssn",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\x00?\xd7\xdc\xa5LL=\xbc\x9a\xb0\xe7:.\xb3>", 4),
            },
            {
                "bsonType": "date",
                "path": "birth_date",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\xd6\xaf\xd7*u\xe6E\x81\xa3!\xe3C\xf0;\x87\xb7", 4),
            },
            {
                "bsonType": "binData",
                "path": "profile_picture",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xc8\x00\x19\xeaT0Nx\xb1\xd2~3\xa8\xbf|\x0b", 4),
            },
            {
                "bsonType": "int",
                "path": "patient_age",
                "queries": {"queryType": "range"},
                "keyId": Binary(
                    b"<\x9f\x18\xb1$\x94N\x16\x86\xbav\xc3\x93\x90w\xd8", 4
                ),
            },
            {
                "bsonType": "double",
                "path": "weight",
                "queries": {"queryType": "range"},
                "keyId": Binary(b"\xfd\xa3\xeb\xe5\xdf C!\x90\xbb-S\xb5[r/", 4),
            },
        ]
    },
    "test_encrypted.patient": {
        "fields": [
            {
                "bsonType": "int",
                "path": "patient_id",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\xf5\xce;>\xd1`A\x0c\xbd\xb9\x91\x04\x12K*\x9c", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_name",
                "keyId": Binary(b"\xd9\xc3\xff\xbc9~H\xeb\x89 d-\x16i,\xe5", 4),
            },
            {
                "bsonType": "string",
                "path": "patient_notes",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x99\x1a\x0c\xcf\x00\xe0B\x17\x94\xafj*7\x01\xc4\x82", 4
                ),
            },
            {
                "bsonType": "date",
                "path": "registration_date",
                "queries": {"queryType": "equality"},
                "keyId": Binary(
                    b"\x11\x95\xac:\x07;N\xd5\xb1\xc1\xea4\xda&\xa7\xaa", 4
                ),
            },
            {
                "bsonType": "bool",
                "path": "is_active",
                "queries": {"queryType": "equality"},
                "keyId": Binary(b"\x91:\x94\x05\xd2aA\x9d\xbd\x9b\xb0\x07PR=\\", 4),
            },
        ]
    },
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
                schema_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
            )
        },
        db_name="encrypted",
    ),
}
DATABASES["encrypted"]["KMS_CREDENTIALS"] = encryption.KMS_CREDENTIALS

DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
