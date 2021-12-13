from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    VERSION_NOT_FOUND_EXCEPTION,
    KEY_VERSION_NOT_FOUND_EXCEPTION,
    INVALID_SCOPE_EXCEPTION,
    KEY_INVALID_SCOPE_EXCEPTION,
    INVALID_RESOURCE_ID_EXCEPTION,
    KEY_INVALID_RESOURCE_ID_EXCEPTION, MISSING_VERSION_ID_EXCEPTION, KEY_MISSING_VERSION_ID_EXCEPTION,
    MISSING_STEP_ID_EXCEPTION, KEY_MISSING_STEP_ID_EXCEPTION,
)


class VersionNotFoundException(HTTPException):
    def __init__(self, message=VERSION_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_VERSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InvalidScopeException(HTTPException):
    def __init__(self, message=INVALID_SCOPE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_INVALID_SCOPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class InvalidResourceIdException(HTTPException):
    def __init__(self, message=INVALID_RESOURCE_ID_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_INVALID_RESOURCE_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class InvalidThematiqueNameException(HTTPException):
    def __init__(self, message=INVALID_RESOURCE_ID_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_INVALID_RESOURCE_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class MissingVersionIdException(HTTPException):
    def __init__(self, message=MISSING_VERSION_ID_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_MISSING_VERSION_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class MissingStepIdException(HTTPException):
    def __init__(self, message=MISSING_STEP_ID_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_MISSING_STEP_ID_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
