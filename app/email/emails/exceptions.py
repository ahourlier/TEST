from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    EMAIL_NOT_FOUND_EXCEPTION,
    KEY_EMAIL_NOT_FOUND_EXCEPTION,
    EMAIL_MISSING_RECIPIENT_EXCEPTION,
    KEY_EMAIL_MISSING_RECIPIENT_EXCEPTION,
    EMAIL_NOT_INTERNAL_SENDER_EXCEPTION,
    KEY_EMAIL_NOT_INTERNAL_SENDER_EXCEPTION,
)


class EmailNotFoundException(HTTPException):
    def __init__(self, message=EMAIL_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_EMAIL_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class EmailMissingRecipientException(HTTPException):
    def __init__(self, message=EMAIL_MISSING_RECIPIENT_EXCEPTION):
        self.code = 400
        self.key = KEY_EMAIL_MISSING_RECIPIENT_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class EmailNotInternalSenderException(HTTPException):
    def __init__(self, message=EMAIL_NOT_INTERNAL_SENDER_EXCEPTION):
        self.code = 403
        self.key = KEY_EMAIL_NOT_INTERNAL_SENDER_EXCEPTION
        self.message = message
        self.status = "FORBIDDEN"
