from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    PERSON_NOT_FOUND_EXCEPTION,
    KEY_PERSON_NOT_FOUND_EXCEPTION,
)


class PersonNotFoundException(HTTPException):
    def __init__(self, message=PERSON_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_PERSON_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
