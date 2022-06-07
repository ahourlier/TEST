from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    VERSION_NOT_FOUND_EXCEPTION,
    KEY_VERSION_NOT_FOUND_EXCEPTION,
    INVALID_SCOPE_EXCEPTION,
    KEY_INVALID_SCOPE_EXCEPTION,
    INVALID_RESOURCE_ID_EXCEPTION,
    KEY_INVALID_RESOURCE_ID_EXCEPTION,
    MISSING_VERSION_ID_EXCEPTION,
    KEY_MISSING_VERSION_ID_EXCEPTION,
    MISSING_STEP_ID_EXCEPTION,
    KEY_MISSING_STEP_ID_EXCEPTION,
    STEP_NOT_FOUND_EXCEPTION,
    KEY_STEP_NOT_FOUND_EXCEPTION,
    KEY_VERSION_DELETION_UNAUTHORIZED,
    VERSION_DELETION_UNAUTHORIZED,
    KEY_VERSION_UPDATE_UNAUTHORIZED,
    VERSION_UPDATE_UNAUTHORIZED,
    KEY_VERSION_DUPLICATION_UNAUTHORIZED,
    VERSION_DUPLICATION_UNAUTHORIZED,
    KEY_NOT_UNIQUE_DATA_AND_NAME_VERSION_UNAUTHORIZED,
    NOT_UNIQUE_DATA_AND_NAME_VERSION_UNAUTHORIZED,
)


class VersionNotFoundException(HTTPException):
    def __init__(self, message=VERSION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_VERSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class StepNotFoundException(HTTPException):
    def __init__(self, message=STEP_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_STEP_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InvalidScopeException(HTTPException):
    def __init__(self, message=INVALID_SCOPE_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_SCOPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class InvalidResourceIdException(HTTPException):
    def __init__(self, message=INVALID_RESOURCE_ID_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_RESOURCE_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class InvalidThematiqueNameException(HTTPException):
    def __init__(self, message=INVALID_RESOURCE_ID_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_RESOURCE_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class MissingVersionIdException(HTTPException):
    def __init__(self, message=MISSING_VERSION_ID_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_VERSION_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class MissingStepIdException(HTTPException):
    def __init__(self, message=MISSING_STEP_ID_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_STEP_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class UnauthorizedToDeleteException(HTTPException):
    def __init__(self, message=VERSION_DELETION_UNAUTHORIZED):
        self.code = 401
        self.key = KEY_VERSION_DELETION_UNAUTHORIZED
        self.message = message
        self.status = "UNAUTHORIZED"


class UnauthorizedToUpdateException(HTTPException):
    def __init__(self, message=VERSION_UPDATE_UNAUTHORIZED):
        self.code = 401
        self.key = KEY_VERSION_UPDATE_UNAUTHORIZED
        self.message = message
        self.status = "UNAUTHORIZED"


class UnauthorizedDuplicationException(HTTPException):
    def __init__(self, message=VERSION_DUPLICATION_UNAUTHORIZED):
        self.code = 401
        self.key = KEY_VERSION_DUPLICATION_UNAUTHORIZED
        self.message = message
        self.status = "UNAUTHORIZED"


class NotUniqueDataAndNameVersionException(HTTPException):
    def __init__(self, message=NOT_UNIQUE_DATA_AND_NAME_VERSION_UNAUTHORIZED):
        self.code = 401
        self.key = KEY_NOT_UNIQUE_DATA_AND_NAME_VERSION_UNAUTHORIZED
        self.message = message
        self.status = "UNAUTHORIZED"
