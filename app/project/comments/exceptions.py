from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    COMMENT_NOT_FOUND_EXCEPTION,
    KEY_COMMENT_NOT_FOUND_EXCEPTION,
)


class CommentNotFoundException(HTTPException):
    def __init__(self, message=COMMENT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_COMMENT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
