from . import api
from .exceptions import HotWaterNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(HotWaterNotFoundException)
def hot_water_not_found(error):  # pragma: no cover
    return parse_exception(error)
