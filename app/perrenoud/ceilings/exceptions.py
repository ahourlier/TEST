from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    CEILING_NOT_FOUND_EXCEPTION,
    KEY_CEILING_NOT_FOUND_EXCEPTION,
)


class CeilingNotFoundException(HTTPException):
    def __init__(self, message=CEILING_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CEILING_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
