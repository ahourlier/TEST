from . import api
from .exceptions import (
    QuoteNotFoundException,
    WorkTypeNotFoundException,
    QuoteAccommodationNotFoundException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(QuoteNotFoundException)
def quote_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WorkTypeNotFoundException)
def work_type_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(QuoteAccommodationNotFoundException)
def quote_accommodation_not_found(error):  # pragma: no cover
    return parse_exception(error)
