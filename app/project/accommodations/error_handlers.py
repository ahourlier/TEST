from . import api
from .exceptions import AccommodationNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(AccommodationNotFoundException)
def accommodation_not_found(error):  # pragma: no cover
    return parse_exception(error)
