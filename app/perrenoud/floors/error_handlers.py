from . import api
from .exceptions import FloorNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(FloorNotFoundException)
def floor_not_found(error):  # pragma: no cover
    return parse_exception(error)
