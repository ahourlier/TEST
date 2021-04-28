from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    WORK_TYPE_NOT_FOUND_EXCEPTION,
    KEY_WORK_TYPE_NOT_FOUND_EXCEPTION,
)


class WorkTypeNotFoundException(HTTPException):
    def __init__(self, message=WORK_TYPE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_WORK_TYPE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
