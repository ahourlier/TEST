from . import api
from .exceptions import (
    DisorderNotFoundException,
    DisorderTypeNotFoundException,
    InvalidDisorderJoinException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(DisorderNotFoundException)
def disorder_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(DisorderTypeNotFoundException)
def disorder_type_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidDisorderJoinException)
def invalid_disorder_join(error):  # pragma: no cover
    return parse_exception(error)
