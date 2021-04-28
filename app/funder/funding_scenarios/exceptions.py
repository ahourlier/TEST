from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    FUNDING_SCENARIO_NOT_FOUND_EXCEPTION,
    KEY_FUNDING_SCENARIO_NOT_FOUND_EXCEPTION,
    FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION,
    KEY_FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION,
)


class FundingScenarioNotFoundException(HTTPException):
    def __init__(self, message=FUNDING_SCENARIO_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_FUNDING_SCENARIO_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class FundingScenarioFunderChangeException(HTTPException):
    def __init__(self, message=FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION):
        self.code = 400
        self.key = KEY_FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
