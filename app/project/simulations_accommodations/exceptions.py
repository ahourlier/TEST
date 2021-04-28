from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION,
    ACCOMMODATION_ALREADY_USED_EXCEPTION,
    KEY_ACCOMMODATION_ALREADY_USED_EXCEPTION,
)


class SimulationAccommodationNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationAlreadyUsedException(HTTPException):
    def __init__(self, message=ACCOMMODATION_ALREADY_USED_EXCEPTION):
        self.code = 400
        self.key = KEY_ACCOMMODATION_ALREADY_USED_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
