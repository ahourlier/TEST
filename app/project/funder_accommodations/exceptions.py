from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION,
    KEY_FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION,
)


class FunderAccommodationsNotFoundException(HTTPException):
    def __init__(self, message=FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
