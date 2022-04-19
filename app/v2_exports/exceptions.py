from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    MISSION_NOT_FOUND_EXCEPTION,
    KEY_MISSION_NOT_FOUND_EXCEPTION,
    EXPORT_NOT_FOUND_EXCEPTION,
    KEY_EXPORT_NOT_FOUND_EXCEPTION,
    LOG_SHEET_NOT_CREATED_EXCEPTION,
    KEY_LOG_SHEET_NOT_CREATED_EXCEPTION,
)


class MissionNotFoundException(HTTPException):
    def __init__(self, message=MISSION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_MISSION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class ExportNotFoundException(HTTPException):
    def __init__(self, message=EXPORT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_EXPORT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class LogSheetNotCreatedException(HTTPException):
    def __init__(self, message=LOG_SHEET_NOT_CREATED_EXCEPTION):
        self.code = 500
        self.key = KEY_LOG_SHEET_NOT_CREATED_EXCEPTION
        self.message = message
        self.status = "INTERNAL SERVER ERROR"
