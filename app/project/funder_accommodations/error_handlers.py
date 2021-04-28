from . import api

from app.common.error_handlers import parse_exception
from .exceptions import FunderAccommodationsNotFoundException


@api.errorhandler(FunderAccommodationsNotFoundException)
def funder_accommodations_not_found(error):  # pragma: no cover
    return parse_exception(error)
