from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    HOT_WATER_NOT_FOUND_EXCEPTION,
    KEY_HOT_WATER_NOT_FOUND_EXCEPTION,
)


class HotWaterNotFoundException(HTTPException):
    def __init__(self, message=HOT_WATER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_HOT_WATER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
