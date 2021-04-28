from . import api
from .exceptions import AreaNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(AreaNotFoundException)
def area_not_found(error):  # pragma: no cover
    return parse_exception(error)
