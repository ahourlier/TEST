from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    QUOTE_NOT_FOUND_EXCEPTION,
    KEY_QUOTE_NOT_FOUND_EXCEPTION,
    WORK_TYPE_NOT_FOUND_EXCEPTION,
    KEY_WORK_TYPE_NOT_FOUND_EXCEPTION,
    QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION,
    KEY_QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION,
)


class QuoteNotFoundException(HTTPException):
    def __init__(self, message=QUOTE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_QUOTE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class WorkTypeNotFoundException(HTTPException):
    def __init__(self, message=WORK_TYPE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_WORK_TYPE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class QuoteAccommodationNotFoundException(HTTPException):
    def __init__(self, message=QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
