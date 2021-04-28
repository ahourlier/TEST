from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    THERMAL_BRIDGE_NOT_FOUND_EXCEPTION,
    KEY_THERMAL_BRIDGE_NOT_FOUND_EXCEPTION,
)


class ThermalBridgeNotFoundException(HTTPException):
    def __init__(self, message=THERMAL_BRIDGE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_THERMAL_BRIDGE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
