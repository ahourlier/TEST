from . import api
from .exceptions import (
    FunderNotFoundException,
    FunderMissionChangeException,
    FunderUsedBySimulationException,
)

from app.common.error_handlers import parse_exception


@api.errorhandler(FunderNotFoundException)
def funder_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(FunderMissionChangeException)
def funder_mission_change(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(FunderUsedBySimulationException)
def funder_used_simulation(error):  # pragma: no cover
    return parse_exception(error)
