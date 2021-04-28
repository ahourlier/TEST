from . import api
from .exceptions import CeilingNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(CeilingNotFoundException)
def ceiling_not_found(error):  # pragma: no cover
    return parse_exception(error)
