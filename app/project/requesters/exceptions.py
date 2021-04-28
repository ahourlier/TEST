from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    REQUESTER_NOT_FOUND_EXCEPTION,
    KEY_REQUESTER_NOT_FOUND_EXCEPTION,
    REQUESTER_TYPE_CONSTANT_EXCEPTION,
    KEY_REQUESTER_TYPE_CONSTANT_EXCEPTION,
)


class RequesterNotFoundException(HTTPException):
    def __init__(self, message=REQUESTER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_REQUESTER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class RequesterTypeConstantException(HTTPException):
    def __init__(self, message=REQUESTER_TYPE_CONSTANT_EXCEPTION):
        self.code = 400
        self.key = KEY_REQUESTER_TYPE_CONSTANT_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
