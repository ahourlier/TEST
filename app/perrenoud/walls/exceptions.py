from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    OUTSIDE_WALL_NOT_FOUND_EXCEPTION,
    KEY_OUTSIDE_WALL_NOT_FOUND_EXCEPTION,
)


class WallNotFoundException(HTTPException):
    def __init__(self, message=OUTSIDE_WALL_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_OUTSIDE_WALL_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
