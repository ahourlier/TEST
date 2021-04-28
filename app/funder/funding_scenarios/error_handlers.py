from . import api
from .exceptions import (
    FundingScenarioNotFoundException,
    FundingScenarioFunderChangeException,
)

from app.common.error_handlers import parse_exception


@api.errorhandler(FundingScenarioNotFoundException)
def funding_scenario_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(FundingScenarioFunderChangeException)
def funding_scenario_funder_change(error):  # pragma: no cover
    return parse_exception(error)
