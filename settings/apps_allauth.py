from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig
from allauth.usersessions.apps import UserSessionsConfig
from allauth.mfa.apps import MFAConfig


class MongoMFAConfig(MFAConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"


class MongoUserSessionsConfig(UserSessionsConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"


class MongoAccountConfig(AccountConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"


class MongoSocialAccountConfig(SocialAccountConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
