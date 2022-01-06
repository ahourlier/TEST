from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    TASK_NOT_FOUND_EXCEPTION,
    KEY_TASK_NOT_FOUND_EXCEPTION,
    BAD_FORMAT_ASSIGNEE_EXCEPTION,
    KEY_BAD_FORMAT_ASSIGNEE_EXCEPTION,
)


class TaskNotFoundException(HTTPException):
    def __init__(self, message=TASK_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_TASK_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class BadFormatAssigneeException(HTTPException):
    def __init__(self, message=BAD_FORMAT_ASSIGNEE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_BAD_FORMAT_ASSIGNEE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
