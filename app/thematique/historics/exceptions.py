from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    CREATE_HISTORIC_EXCEPTION,
    KEY_CREATE_HISTORIC_EXCEPTION,
    HISTORIC_NOT_FOUND_EXCEPTION,
    KEY_HISTORIC_NOT_FOUND_EXCEPTION,
)


class CreateHistoricException(HTTPException):
    def __init__(self, message=CREATE_HISTORIC_EXCEPTION):
        self.code = 400
        self.key = KEY_CREATE_HISTORIC_EXCEPTION
        self.message = message
        self.status = "CREATE FAILED"


class HistoricNotFoundException(HTTPException):
    def __init__(self, message=HISTORIC_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_HISTORIC_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
