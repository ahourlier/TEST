from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SYNDIC_NOT_FOUND_EXCEPTION,
    KEY_SYNDIC_NOT_FOUND_EXCEPTION,
    MISSION_NOT_TYPE_SYNDIC_EXCEPTION,
    KEY_MISSION_NOT_TYPE_SYNDIC_EXCEPTION,
)


class SyndicNotFoundException(HTTPException):
    def __init__(self, message=SYNDIC_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_SYNDIC_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"

