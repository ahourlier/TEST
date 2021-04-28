from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    COMMON_AREA_NOT_FOUND_EXCEPTION,
    KEY_COMMON_AREA_NOT_FOUND_EXCEPTION,
    EXISTING_COMMON_AREA_EXCEPTION,
    KEY_EXISTING_COMMON_AREA_EXCEPTION,
)


class CommonAreaNotFoundException(HTTPException):
    def __init__(self, message=COMMON_AREA_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_COMMON_AREA_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class ExistingCommonAreaException(HTTPException):
    def __init__(self, message=EXISTING_COMMON_AREA_EXCEPTION):
        self.code = 400
        self.key = KEY_EXISTING_COMMON_AREA_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
