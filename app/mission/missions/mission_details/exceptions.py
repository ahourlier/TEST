from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    MISSION_NOT_FOUND_EXCEPTION,
    KEY_MISSION_NOT_FOUND_EXCEPTION, UNKNOWN_MISSION_TYPE_EXCEPTION, KEY_UNKNOWN_MISSION_TYPE_EXCEPTION,
)


class MissionDetailNotFoundException(HTTPException):
    def __init__(self, message=MISSION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_MISSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
