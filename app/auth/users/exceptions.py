from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    USER_NOT_FOUND_EXCEPTION,
    KEY_USER_NOT_FOUND_EXCEPTION,
    UNKNOWN_CONNEXION_EMAIL,
    KEY_UNKNOWN_CONNEXION_EMAIL,
    INACTIVE_USER,
    KEY_INACTIVE_USER,
)


class UserNotFoundException(HTTPException):
    def __init__(self, message=USER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_USER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InactiveUser(HTTPException):
    def __init__(self, message=INACTIVE_USER):
        self.code = 401
        self.key = KEY_INACTIVE_USER
        self.message = message
        self.status = "UNAUTHORIZED"


class UnknownConnexionEmail(HTTPException):
    def __init__(self, message=UNKNOWN_CONNEXION_EMAIL):
        self.code = 401
        self.key = KEY_UNKNOWN_CONNEXION_EMAIL
        self.message = message
        self.status = "UNAUTHORIZED"
