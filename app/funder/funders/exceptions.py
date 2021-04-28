from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FUNDER_NOT_FOUND_EXCEPTION,
    KEY_FUNDER_NOT_FOUND_EXCEPTION,
    FUNDER_MISSION_CHANGE_EXCEPTION,
    KEY_FUNDER_MISSION_CHANGE_EXCEPTION,
    FUNDER_USED_BY_SIMULATION_EXCEPTION,
    KEY_FUNDER_USED_BY_SIMULATION_EXCEPTION,
)


class FunderNotFoundException(HTTPException):
    def __init__(self, message=FUNDER_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_FUNDER_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class FunderUsedBySimulationException(HTTPException):
    def __init__(self, message=FUNDER_USED_BY_SIMULATION_EXCEPTION):
        self.code = 400
        self.key = KEY_FUNDER_USED_BY_SIMULATION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class FunderMissionChangeException(HTTPException):
    def __init__(self, message=FUNDER_MISSION_CHANGE_EXCEPTION):
        self.code = 400
        self.key = KEY_FUNDER_MISSION_CHANGE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
