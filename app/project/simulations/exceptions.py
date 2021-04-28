from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SIMULATION_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_NOT_FOUND_EXCEPTION,
    USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION,
    KEY_USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION,
    SIMULATION_QUOTE_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_QUOTE_NOT_FOUND_EXCEPTION,
    SIMULATION_FUNDER_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_FUNDER_NOT_FOUND_EXCEPTION,
    SIMULATION_USED_EXCEPTION,
    KEY_SIMULATION_USED_EXCEPTION,
    CLONE_FUNDER_EXCEPTION,
    KEY_CLONE_FUNDER_EXCEPTION,
)


class SimulationNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class UseCaseSimulationNotFoundException(HTTPException):
    def __init__(self, message=USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationQuoteNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_QUOTE_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_QUOTE_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationFunderNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_FUNDER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_FUNDER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationUsedException(HTTPException):
    def __init__(self, message=SIMULATION_USED_EXCEPTION):
        self.code = 400
        self.key = KEY_SIMULATION_USED_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class CloneFunderException(HTTPException):
    def __init__(self, message=CLONE_FUNDER_EXCEPTION):
        self.code = 400
        self.key = KEY_CLONE_FUNDER_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
