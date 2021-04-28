from . import api
from .exceptions import WoodworkNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(WoodworkNotFoundException)
def woodwork_not_found(error):  # pragma: no cover
    return parse_exception(error)
