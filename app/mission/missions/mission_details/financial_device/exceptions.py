from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FINANCIAL_DEVICE_NOT_FOUND_EXCEPTION,
    KEY_FINANCIAL_DEVICE_NOT_FOUND_EXCEPTION,
)


class FinancialDeviceNotFoundException(HTTPException):
    def __init__(self, message=FINANCIAL_DEVICE_NOT_FOUND_EXCEPTION):
        super().__init__()
        self.code = 404
        self.key = KEY_FINANCIAL_DEVICE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
