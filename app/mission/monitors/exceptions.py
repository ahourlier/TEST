from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    MONITOR_NOT_FOUND_EXCEPTION,
    KEY_MONITOR_NOT_FOUND_EXCEPTION,
    MONITOR_FIELD_NOT_FOUND_EXCEPTION,
    KEY_MONITOR_FIELD_NOT_FOUND_EXCEPTION,
)


class MonitorNotFoundException(HTTPException):
    def __init__(self, message=MONITOR_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_MONITOR_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class MonitorFieldNotFoundException(HTTPException):
    def __init__(self, message=MONITOR_FIELD_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_MONITOR_FIELD_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
