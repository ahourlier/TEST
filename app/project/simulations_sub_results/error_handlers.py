from . import api
from app.common.error_handlers import parse_exception
from .exceptions import SimulationSubResultNotFoundException


@api.errorhandler(SimulationSubResultNotFoundException)
def simulation_sub_result_not_found(error):  # pragma: no cover
    return parse_exception(error)
