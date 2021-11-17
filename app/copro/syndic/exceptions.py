from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SYNDIC_NOT_FOUND_EXCEPTION,
    KEY_SYNDIC_NOT_FOUND_EXCEPTION, WRONG_SYNDIC_TYPE_EXCEPTION, KEY_WRONG_SYNDIC_TYPE_EXCEPTION,
)


class SyndicNotFoundException(HTTPException):
    def __init__(self, message=SYNDIC_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_SYNDIC_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class WrongSyndicTypeException(HTTPException):
    def __init__(self, message=WRONG_SYNDIC_TYPE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_SYNDIC_TYPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
