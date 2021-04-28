from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION,
    KEY_PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION,
    CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION,
    KEY_CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION,
)


class ProjectCustomFieldNotFoundException(HTTPException):
    def __init__(self, message=PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class CustomFieldValueNotFoundException(HTTPException):
    def __init__(self, message=CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
