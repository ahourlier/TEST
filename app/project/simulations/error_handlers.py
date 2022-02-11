from . import api
from app.common.error_handlers import parse_exception
from .exceptions import (
    InconsistentScenarioException,
    SimulationNotFoundException,
    UseCaseSimulationNotFoundException,
    SimulationQuoteNotFoundException,
    SimulationFunderNotFoundException,
    SimulationUsedException,
    CloneFunderException,
)


@api.errorhandler(SimulationNotFoundException)
def simulation_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UseCaseSimulationNotFoundException)
def use_case_simulation_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationQuoteNotFoundException)
def simulation_quote_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationFunderNotFoundException)
def simulation_funder_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationUsedException)
def simulation_used(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(CloneFunderException)
def clone_funder(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InconsistentScenarioException)
def inconsistent_scenario(error):  # pragma: no cover
    return parse_exception(error)
