from flask import current_app
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from google.oauth2 import service_account


class GoogleRestService:
    """Wrapper for Google Services"""

    def __init__(
        self,
        service_name,
        service_version,
        scopes,
        user_email=None,
    ):
        self.user_email = user_email
        self.service_name = service_name
        self.service_version = service_version
        self.private_key_path = current_app.config[
            "GAPI_SERVICE_ACCOUNT_PRIVATE_KEY_PATH"
        ]
        self.scopes = [scopes] if not isinstance(scopes, list) else scopes
        self.service = None

    @staticmethod
    def get_request_builder():
        return HttpRequest

    @staticmethod
    def get_http():
        pass

    def __get_credentials(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.private_key_path, scopes=self.scopes
        )
        if self.user_email is not None:
            return credentials.with_subject(self.user_email)
        return credentials

    def __authorize_google_api(self):
        if self.service is None:
            http = self.get_http() if current_app.config["TESTING"] else None
            credentials = (
                self.__get_credentials() if not current_app.config["TESTING"] else None
            )
            self.service = build(
                self.service_name,
                self.service_version,
                credentials=credentials,
                http=http,
                cache_discovery=False,
                requestBuilder=self.get_request_builder(),
            )
        return self.service

    def get(self):
        return self.__authorize_google_api()


class DirectoryService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "admin",
            "directory_v1",
            current_app.config["GAPI_DIRECTORY_SCOPES"],
            user_email=user_email,
        )


class DriveService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "drive",
            "v3",
            current_app.config["GAPI_DRIVE_SCOPES"],
            user_email=user_email,
        )


class GroupsSettingsService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "groupssettings",
            "v1",
            current_app.config["GAPI_GROUPS_SCOPES"],
            user_email=user_email,
        )


class GMailService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "gmail",
            "v1",
            current_app.config["GAPI_GMAIL_SCOPES"],
            user_email=user_email,
        )


class DocsService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "docs",
            "v1",
            current_app.config["GAPI_DRIVE_SCOPES"],
            user_email=user_email,
        )


class SheetsService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "sheets",
            "v4",
            current_app.config["GAPI_DRIVE_SCOPES"],
            user_email=user_email,
        )


class CloudIdentityService(GoogleRestService):
    def __init__(self, user_email):
        super().__init__(
            "cloudidentity",
            "v1",
            current_app.config["CLOUD_IDENTITY_SCOPES"],
            user_email=user_email,
        )
