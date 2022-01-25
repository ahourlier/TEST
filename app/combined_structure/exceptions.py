from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    BUILDING_NOT_FOUND_EXCEPTION,
    KEY_BUILDING_NOT_FOUND_EXCEPTION,
)


class CombinedStructureNotFoundException(HTTPException):
    def __init__(self, message=BUILDING_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_BUILDING_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
