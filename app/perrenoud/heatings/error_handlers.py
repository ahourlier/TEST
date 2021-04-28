from . import api
from .exceptions import HeatingNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(HeatingNotFoundException)
def heating_not_found(error):  # pragma: no cover
    return parse_exception(error)
