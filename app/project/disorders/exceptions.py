from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    DISORDER_NOT_FOUND_EXCEPTION,
    KEY_DISORDER_NOT_FOUND_EXCEPTION,
    DISORDER_TYPE_NOT_FOUND_EXCEPTION,
    KEY_DISORDER_TYPE_NOT_FOUND_EXCEPTION,
    INVALID_DISORDER_JOINS_EXCEPTION,
    KEY_INVALID_DISORDER_JOINS_EXCEPTION,
)


class DisorderNotFoundException(HTTPException):
    def __init__(self, message=DISORDER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_DISORDER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class DisorderTypeNotFoundException(HTTPException):
    def __init__(self, message=DISORDER_TYPE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_DISORDER_TYPE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InvalidDisorderJoinException(HTTPException):
    def __init__(self, message=INVALID_DISORDER_JOINS_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_DISORDER_JOINS_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
