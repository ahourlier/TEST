from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    AREA_NOT_FOUND_EXCEPTION,
    KEY_AREA_NOT_FOUND_EXCEPTION,
)


class AreaNotFoundException(HTTPException):
    def __init__(self, message=AREA_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_AREA_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
