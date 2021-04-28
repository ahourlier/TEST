from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    HEATING_NOT_FOUND_EXCEPTION,
    KEY_HEATING_NOT_FOUND_EXCEPTION,
)


class HeatingNotFoundException(HTTPException):
    def __init__(self, message=HEATING_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_HEATING_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
