from django_mongodb_backend.utils import model_has_encrypted_fields


class EncryptionRouter:
    def db_for_read(self, model, **hints):
        if model_has_encrypted_fields(model):
            return "encrypted"
        return "default"

    def db_for_write(self, model, **hints):
        if model_has_encrypted_fields(model):
            return "encrypted"
        return "default"

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
