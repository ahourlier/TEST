from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SEARCH_NOT_FOUND_EXCEPTION,
    KEY_SEARCH_NOT_FOUND_EXCEPTION,
)


class SearchNotFoundException(HTTPException):
    def __init__(self, message=SEARCH_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SEARCH_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
