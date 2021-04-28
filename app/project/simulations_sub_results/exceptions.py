from http.client import HTTPException

from app.common.config_error_messages import (
    SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION,
)


class SimulationSubResultNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
