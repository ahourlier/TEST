from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    ACCOMMODATION_NOT_FOUND_EXCEPTION,
    KEY_ACCOMMODATION_NOT_FOUND_EXCEPTION,
)


class AccommodationNotFoundException(HTTPException):
    def __init__(self, message=ACCOMMODATION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_ACCOMMODATION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
