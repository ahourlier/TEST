from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    PROJECT_LEAD_NOT_FOUND_EXCEPTION,
    KEY_PROJECT_LEAD_NOT_FOUND_EXCEPTION,
    UNIDENTIFIED_REFERRER_EXCEPTION,
    KEY_UNIDENTIFIED_REFERRER_EXCEPTION,
)


class ProjectLeadNotFoundException(HTTPException):
    def __init__(self, message=PROJECT_LEAD_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_PROJECT_LEAD_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class UnidentifiedReferrerException(HTTPException):
    def __init__(self, message=UNIDENTIFIED_REFERRER_EXCEPTION):
        self.code = 404
        self.key = KEY_UNIDENTIFIED_REFERRER_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
