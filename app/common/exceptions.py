from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    INCONSISTENT_UPDATE_ID_DEFAULT,
    KEY_INCONSISTENT_UPDATE_ID_DEFAULT,
    FORBIDDEN_EXCEPTION,
    KEY_FORBIDDEN_EXCEPTION,
    INVALID_SEARCH_OPERATOR_EXCEPTION,
    KEY_INVALID_SEARCH_OPERATOR_EXCEPTION,
    INVALID_SEARCH_FIELD_EXCEPTION,
    KEY_INVALID_SEARCH_FIELD_EXCEPTION,
    CHILD_MISSION_EXCEPTION,
    KEY_CHILD_MISSION_EXCEPTION,
    VALIDATION_ERRORS,
    SHARED_DRIVE_ERRORS,
    GOOGLE_GROUPS_ERRORS,
    INVALID_PARAMS_REQUEST_EXCEPTION,
    KEY_INVALID_PARAMS_REQUEST_EXCEPTION,
    XML_GENERATION_ERRORS,
    INVALID_FILE_EXCEPTION,
    KEY_INVALID_FILE_EXCEPTION,
    WRONG_ENUM_TYPE_EXCEPTION, KEY_WRONG_ENUM_TYPE_EXCEPTION,
)


class InconsistentUpdateIdException(HTTPException):
    def __init__(self, message=INCONSISTENT_UPDATE_ID_DEFAULT):
        self.code = 400
        self.key = KEY_INCONSISTENT_UPDATE_ID_DEFAULT
        self.message = message
        self.status = "BAD REQUEST"


class InvalidParamsRequestException(HTTPException):
    def __init__(self, message=INVALID_PARAMS_REQUEST_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_PARAMS_REQUEST_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ForbiddenException(HTTPException):
    def __init__(self, message=FORBIDDEN_EXCEPTION):
        self.code = 403
        self.key = KEY_FORBIDDEN_EXCEPTION
        self.message = message
        self.status = "FORBIDDEN"


class InvalidSearchOperatorException(HTTPException):
    def __init__(self, message=INVALID_SEARCH_OPERATOR_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_SEARCH_OPERATOR_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class InvalidSearchFieldException(HTTPException):
    def __init__(self, message=INVALID_SEARCH_FIELD_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_SEARCH_FIELD_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ChildMissionException(HTTPException):
    def __init__(self, message=CHILD_MISSION_EXCEPTION):
        self.code = 400
        self.key = KEY_CHILD_MISSION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ValidationException(HTTPException):
    def __init__(self, message=None):
        self.code = 400
        self.key = message
        self.message = (
            VALIDATION_ERRORS.get(message, "A validation error occurred")
            if message
            else "A validation error occurred"
        )
        self.status = "BAD REQUEST"


class SharedDriveException(HTTPException):
    def __init__(self, message=None):
        self.code = 500
        self.key = message
        self.message = (
            SHARED_DRIVE_ERRORS.get(message, "An error occurred in Google Drive")
            if message
            else "An error occurred in Google Drive"
        )
        self.status = "INTERNAL_SERVER_ERROR"


class GoogleGroupsException(HTTPException):
    def __init__(self, message=None):
        self.code = 500
        self.key = message
        self.message = (
            GOOGLE_GROUPS_ERRORS.get(message, "An error occurred with Google Groups")
            if message
            else "An error occurred with Google Groups"
        )
        self.status = "INTERNAL_SERVER_ERROR"


class GoogleDocsException(HTTPException):
    def __init__(self, message=None):
        self.code = 500
        self.key = message
        self.message = (
            SHARED_DRIVE_ERRORS.get(message, "An error occurred in Google Docs")
            if message
            else "An error occurred in Google Docs"
        )
        self.status = "INTERNAL_SERVER_ERROR"


class GoogleSheetsException(HTTPException):
    def __init__(self, message=None):
        self.code = 500
        self.key = message
        self.message = (
            SHARED_DRIVE_ERRORS.get(message, "An error occurred in Google Sheets")
            if message
            else "An error occurred in Google Sheets"
        )
        self.status = "INTERNAL_SERVER_ERROR"


class XMLGenerationException(HTTPException):
    def __init__(self, message=None, item_name=None):
        self.code = 500
        self.key = message
        message = (
            XML_GENERATION_ERRORS.get(
                message, "An error occurred during the XML Generation"
            )
            if message
            else "An error occurred during the XML Generation"
        )
        self.message = f"{item_name} : {message}" if item_name else message
        self.status = "INTERNAL_SERVER_ERROR"


class InvalidFileException(HTTPException):
    def __init__(self, message=INVALID_FILE_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_FILE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class EnumException(HTTPException):
    def __init__(
            self,
            message=WRONG_ENUM_TYPE_EXCEPTION,
            value=None,
            enum=None,
            allowed_values="",
            details=None
    ):
        message = message.format(value=value, enum=enum, allowed_values=allowed_values)
        self.code = 400
        self.key = KEY_WRONG_ENUM_TYPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
        self.details = details
