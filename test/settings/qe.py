import os


from django_mongodb_backend import parse_uri
from pymongo.encryption import AutoEncryptionOpts
from django_mongodb_backend.model_utils import model_has_encrypted_fields


MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DATABASES = {
    "default": parse_uri(
        MONGODB_URI,
        db_name="test",
    ),
    "encrypted": parse_uri(
        MONGODB_URI,
        options={
            "auto_encryption_opts": AutoEncryptionOpts(
                key_vault_namespace="encrypted.keyvault",
                kms_providers={
                    "local": {"key": os.urandom(96)},
                },
                # schema_map=EXPECTED_ENCRYPTED_FIELDS_MAP,
            )
        },
        db_name="encrypted",
    ),
}


class EncryptedRouter:
    def db_for_read(self, model, **hints):
        if model_has_encrypted_fields(model):
            return "encrypted"
        return "default"

    def db_for_write(self, model, **hints):
        if model_has_encrypted_fields(model):
            return "encrypted"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = self.db_for_read(obj1.__class__)
        db_obj2 = self.db_for_read(obj2.__class__)
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if hints.get("model"):
            if model_has_encrypted_fields(hints["model"]):
                return db == "encrypted"
            else:
                return db == "default"
        return None

    def kms_provider(self, model):
        if model_has_encrypted_fields(model):
            return "local"
        return None


DATABASE_ROUTERS = [EncryptedRouter()]
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
SECRET_KEY = "django_tests_secret_key"
USE_TZ = False
