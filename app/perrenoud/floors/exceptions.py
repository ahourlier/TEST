from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FLOOR_NOT_FOUND_EXCEPTION,
    KEY_FLOOR_NOT_FOUND_EXCEPTION,
)


class FloorNotFoundException(HTTPException):
    def __init__(self, message=FLOOR_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_FLOOR_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
