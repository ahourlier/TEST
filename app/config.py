import os
import pathlib

from typing import List, Type

base_dir = pathlib.Path(__file__).parent.absolute()


class BaseConfig:
    CONFIG_NAME = "base"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY_PATH = str(
        pathlib.PurePath.joinpath(base_dir, "firebase-key.json")
    )
    GAPI_SERVICE_ACCOUNT_PRIVATE_KEY_PATH = str(
        pathlib.PurePath.joinpath(base_dir, "sa-key.json")
    )
    GAPI_DIRECTORY_USERS_READONLY_SCOPE = (
        "https://www.googleapis.com/auth/admin.directory.user.readonly"
    )

    GAPI_DIRECTORY_GROUPS_SCOPE = (
        "https://www.googleapis.com/auth/admin.directory.group"
    )

    GAPI_GROUPS_SETTINGS_SCOPE = "https://www.googleapis.com/auth/apps.groups.settings"

    GAPI_GROUPS_SCOPES = [GAPI_GROUPS_SETTINGS_SCOPE]

    GAPI_DIRECTORY_SCOPES = [
        GAPI_DIRECTORY_USERS_READONLY_SCOPE,
        GAPI_DIRECTORY_GROUPS_SCOPE,
    ]

    GAPI_DRIVE_FULL_SCOPE = "https://www.googleapis.com/auth/drive"
    GAPI_DRIVE_SCOPES = [GAPI_DRIVE_FULL_SCOPE]

    GAPI_GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
    GAPI_GMAIL_SCOPES = [GAPI_GMAIL_SEND_SCOPE]

    CLOUD_IDENTITY_GROUPS_SCOPE = (
        "https://www.googleapis.com/auth/cloud-identity.groups.readonly"
    )
    CLOUD_IDENTITY_SCOPES = [CLOUD_IDENTITY_GROUPS_SCOPE]

    FLASK_ADMIN_SWATCH = "paper"
    BABEL_DEFAULT_LOCALE = "fr"

    IDENTITY_TOOLKIT_API_BASE_URL = "https://identitytoolkit.googleapis.com/v1/"


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False
    TRANSLATION_URL = (
        "https://storage.googleapis.com/app-oslo-dev-locales/oslo-fr-FR.json"
    )


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:root@127.0.0.1:5432/oslo-test"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    DEBUG = False
    TESTING = False


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
