from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SUBCONTRACTOR_NOT_FOUND_EXCEPTION,
    KEY_SUBCONTRACTOR_NOT_FOUND_EXCEPTION,
)


class SubcontractorNotFoundException(HTTPException):
    def __init__(self):
        super().__init__()
        self.code = 404
        self.key = KEY_SUBCONTRACTOR_NOT_FOUND_EXCEPTION
        self.message = SUBCONTRACTOR_NOT_FOUND_EXCEPTION
        self.status = "NOT FOUND"
