from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    KEY_USER_NOT_FOUND_EXCEPTION, PREFERRED_APP_NOT_FOUND,
)


class PreferredAppFoundException(HTTPException):
    def __init__(self, message=PREFERRED_APP_NOT_FOUND):
        self.code = 404
        self.key = KEY_USER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"

