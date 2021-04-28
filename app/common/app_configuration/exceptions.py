from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    APP_CONFIG_NOT_FOUND_EXCEPTION,
    KEY_APP_CONFIG_NOT_FOUND_EXCEPTION,
)


class AppConfigNotFoundException(HTTPException):
    def __init__(self, message=APP_CONFIG_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_APP_CONFIG_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
