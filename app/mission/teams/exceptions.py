from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    TEAM_NOT_FOUND_EXCEPTION,
    KEY_TEAM_NOT_FOUND_EXCEPTION,
)


class TeamNotFoundException(HTTPException):
    def __init__(self, message=TEAM_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_TEAM_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
