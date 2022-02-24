from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    KEY_STEP_OR_VERSION_MISSING_EXCEPTION,
    STEP_OR_VERSION_MISSING_EXCEPTION,
    TASK_NOT_FOUND_EXCEPTION,
    KEY_TASK_NOT_FOUND_EXCEPTION,
    BAD_FORMAT_ASSIGNEE_EXCEPTION,
    KEY_BAD_FORMAT_ASSIGNEE_EXCEPTION,
    INVALID_TASK_TYPE_EXCEPTION,
    KEY_INVALID_TASK_TYPE_EXCEPTION,
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


class InvalidTaskTypeException(HTTPException):
    def __init__(self, message=INVALID_TASK_TYPE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_INVALID_TASK_TYPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class StepOrVersionMissingException(HTTPException):
    def __init__(self, message=STEP_OR_VERSION_MISSING_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_STEP_OR_VERSION_MISSING_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"