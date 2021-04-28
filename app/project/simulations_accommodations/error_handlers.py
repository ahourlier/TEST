from . import api

from app.common.error_handlers import parse_exception
from .exceptions import (
    SimulationAccommodationNotFoundException,
    SimulationAlreadyUsedException,
)


@api.errorhandler(SimulationAccommodationNotFoundException)
def quote_accommodation_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationAlreadyUsedException)
def accommodation_already_used_exception(error):  # pragma: no cover
    return parse_exception(error)
