from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    DOCUMENT_NOT_FOUND_EXCEPTION,
    KEY_DOCUMENT_NOT_FOUND_EXCEPTION,
    INVALID_SOURCE_EXCEPTION,
    KEY_INVALID_SOURCE_EXCEPTION,
)


class DocumentNotFoundException(HTTPException):
    def __init__(self, message=DOCUMENT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_DOCUMENT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InvalidSourceException(HTTPException):
    def __init__(self, message=INVALID_SOURCE_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_SOURCE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
