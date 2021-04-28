from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    CUSTOM_FIELD_NOT_FOUND_EXCEPTION,
    KEY_CUSTOM_FIELD_NOT_FOUND_EXCEPTION,
    AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION,
    KEY_AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION,
)


class CustomFieldNotFoundException(HTTPException):
    def __init__(self, message=CUSTOM_FIELD_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CUSTOM_FIELD_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class AvailableFieldValueNotFoundException(HTTPException):
    def __init__(self, message=AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
