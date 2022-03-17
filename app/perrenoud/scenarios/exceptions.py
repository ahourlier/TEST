from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SCENARIO_NOT_FOUND_EXCEPTION,
    KEY_SCENARIO_NOT_FOUND_EXCEPTION,
    EXISTING_INITIAL_STATE_EXCEPTION,
    KEY_EXISTING_INITIAL_STATE_EXCEPTION,
    XML_GENERATION_ERRORS,
    PERRENOUD_WEBSERVICE_EXCEPTION,
    KEY_PERRENOUD_WEBSERVICE_EXCEPTION,
    KEY_MISSING_PERRENOUD_DATA_EXCEPTION,
    MISSING_PERRENOUD_DATA_EXCEPTION,
)


class ScenarioNotFoundException(HTTPException):
    def __init__(self, message=SCENARIO_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SCENARIO_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class MissingPerrenoudDataException(HTTPException):
    def __init__(
        self,
        message=MISSING_PERRENOUD_DATA_EXCEPTION,
        errors_count=0,
        errors=[],
        scenario_name="scenario",
        is_initial_state=False,
    ):
        self.code = 400
        self.key = KEY_MISSING_PERRENOUD_DATA_EXCEPTION
        self.message = message
        self.errors_count = (errors_count,)
        self.errors = errors
        self.status = "NOT FOUND"
        self.scenario_name = scenario_name
        self.is_initial_state = is_initial_state


class InitialStateAlreadyCreatedException(HTTPException):
    def __init__(self, message=EXISTING_INITIAL_STATE_EXCEPTION):
        self.code = 403
        self.key = KEY_EXISTING_INITIAL_STATE_EXCEPTION
        self.message = message
        self.status = "FORBIDDEN"


class PerrenoudWebserviceException(HTTPException):
    def __init__(
        self, message=PERRENOUD_WEBSERVICE_EXCEPTION,
    ):
        self.code = 500
        self.key = KEY_PERRENOUD_WEBSERVICE_EXCEPTION
        self.message = message
        self.status = "INTERNAL"
