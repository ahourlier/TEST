from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    DATA_IMPORT_NOT_FOUND_EXCEPTION,
    KEY_DATA_IMPORT_NOT_FOUND_EXCEPTION,
    INCORRECT_DATA_IMPORT_EXCEPTION,
    KEY_INCORRECT_DATA_IMPORT_EXCEPTION,
    ENTITY_INSERT_FAIL_EXCEPTION,
    KEY_ENTITY_INSERT_FAIL_EXCEPTION,
)


class DataImportNotFoundException(HTTPException):
    def __init__(self, message=DATA_IMPORT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_DATA_IMPORT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class IncorrectDataImportException(HTTPException):
    def __init__(self, message=INCORRECT_DATA_IMPORT_EXCEPTION):
        self.code = 400
        self.key = KEY_INCORRECT_DATA_IMPORT_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class EntityInsertFailException(HTTPException):
    def __init__(self, message=ENTITY_INSERT_FAIL_EXCEPTION):
        self.code = 400
        self.key = KEY_ENTITY_INSERT_FAIL_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
