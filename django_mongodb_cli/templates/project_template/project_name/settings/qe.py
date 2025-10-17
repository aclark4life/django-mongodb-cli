import os

from .base import *  # noqa: F403
from .routers import EncryptionRouter  # noqa: F401
from pymongo.encryption_options import AutoEncryptionOpts

DATABASES["encrypted"] = {  # noqa: F405
    "ENGINE": "django_mongodb_backend",
    "NAME": "encrypted",
    "OPTIONS": {
        "auto_encryption_opts": AutoEncryptionOpts(
            kms_providers={"local": {"key": os.urandom(96)}},
            key_vault_namespace="encryption.__keyVault",
        ),
    },
}

DATABASE_ROUTERS = [EncryptionRouter()]

INSTALLED_APPS += [  # noqa: F405
    "django_mongodb_backend",
]
