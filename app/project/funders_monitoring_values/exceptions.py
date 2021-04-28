from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION,
    KEY_FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION,
)


class FunderMonitoringValueNotFoundException(HTTPException):
    def __init__(self, message=FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
