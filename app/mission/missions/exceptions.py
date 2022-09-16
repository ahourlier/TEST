from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    KEY_WRONG_SHARED_DRIVE_SELECTION_EXCEPTION,
    MISSION_NOT_FOUND_EXCEPTION,
    KEY_MISSION_NOT_FOUND_EXCEPTION,
    UNKNOWN_MISSION_TYPE_EXCEPTION,
    KEY_UNKNOWN_MISSION_TYPE_EXCEPTION,
    WRONG_SHARED_DRIVE_SELECTION_EXCEPTION,
)


class MissionNotFoundException(HTTPException):
    def __init__(self, message=MISSION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_MISSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class UnknownMissionTypeException(HTTPException):
    def __init__(self, message=UNKNOWN_MISSION_TYPE_EXCEPTION):
        self.code = 400
        self.key = KEY_UNKNOWN_MISSION_TYPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongSharedDriveSelectionException(HTTPException):
    def __init__(self, message=WRONG_SHARED_DRIVE_SELECTION_EXCEPTION):
        self.code = 400
        self.key = KEY_WRONG_SHARED_DRIVE_SELECTION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
