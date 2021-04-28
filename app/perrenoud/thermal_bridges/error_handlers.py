from . import api
from .exceptions import ThermalBridgeNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ThermalBridgeNotFoundException)
def thermal_bridge_not_found(error):  # pragma: no cover
    return parse_exception(error)
