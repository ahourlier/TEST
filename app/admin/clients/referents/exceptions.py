from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    REFERENT_NOT_FOUND_EXCEPTION,
    KEY_REFERENT_NOT_FOUND_EXCEPTION,
)


class ReferentNotFoundException(HTTPException):
    def __init__(self, message=REFERENT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_REFERENT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
