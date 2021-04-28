from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    CLIENT_NOT_FOUND_EXCEPTION,
    KEY_CLIENT_NOT_FOUND_EXCEPTION,
    CHILD_CLIENT_MISSION_EXCEPTION,
    KEY_CHILD_CLIENT_MISSION_EXCEPTION,
)


class ClientNotFoundException(HTTPException):
    def __init__(self, message=CLIENT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CLIENT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class ChildClientMissionException(HTTPException):
    def __init__(self, message=CHILD_CLIENT_MISSION_EXCEPTION):
        self.code = 400
        self.key = KEY_CHILD_CLIENT_MISSION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
