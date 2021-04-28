from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    CONTACT_NOT_FOUND_EXCEPTION,
    KEY_CONTACT_NOT_FOUND_EXCEPTION,
)


class ContactNotFoundException(HTTPException):
    def __init__(self, message=CONTACT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CONTACT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
