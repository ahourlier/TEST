from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    VERSION_NOT_FOUND_EXCEPTION, KEY_VERSION_NOT_FOUND_EXCEPTION)


class VersionNotFoundException(HTTPException):
    def __init__(self, message=VERSION_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_VERSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
