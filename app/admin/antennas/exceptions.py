from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    ANTENNA_NOT_FOUND_EXCEPTION,
    KEY_ANTENNA_NOT_FOUND_EXCEPTION,
    ANTENNA_DUPLICATE_NAME_EXCEPTION,
    KEY_ANTENNA_DUPLICATE_NAME_EXCEPTION,
    CHILD_ANTENNA_MISSION_EXCEPTION,
    KEY_CHILD_ANTENNA_MISSION_EXCEPTION,
)


class AntennaNotFoundException(HTTPException):
    def __init__(self, message=ANTENNA_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_ANTENNA_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class AntennaDuplicateNameException(HTTPException):
    def __init__(self, message=ANTENNA_DUPLICATE_NAME_EXCEPTION):
        self.code = 400
        self.key = KEY_ANTENNA_DUPLICATE_NAME_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ChildAntennaMissionException(HTTPException):
    def __init__(self, message=CHILD_ANTENNA_MISSION_EXCEPTION):
        self.code = 400
        self.key = KEY_CHILD_ANTENNA_MISSION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
