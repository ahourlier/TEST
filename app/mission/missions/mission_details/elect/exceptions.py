from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    PARTNER_NOT_FOUND_EXCEPTION,
    KEY_PARTNER_NOT_FOUND_EXCEPTION,
)


class PartnerNotFoundException(HTTPException):
    def __init__(self, message=PARTNER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_PARTNER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
