from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    WOODWORK_NOT_FOUND_EXCEPTION,
    KEY_WOODWORK_NOT_FOUND_EXCEPTION,
)


class WoodworkNotFoundException(HTTPException):
    def __init__(self, message=WOODWORK_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_WOODWORK_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
