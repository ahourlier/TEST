from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    COMBINED_STRUTURE_NOT_FOUND_EXCEPTION,
    KEY_COMBINED_STRUTURE_NOT_FOUND_EXCEPTION,
)


class CombinedStructureNotFoundException(HTTPException):
    def __init__(self, message=COMBINED_STRUTURE_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_COMBINED_STRUTURE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
