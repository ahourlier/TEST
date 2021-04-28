from . import api
from .exceptions import SearchNotFoundException
from app.common.error_handlers import parse_exception
from ...common.exceptions import (
    InvalidSearchOperatorException,
    InvalidSearchFieldException,
)


@api.errorhandler(InvalidSearchOperatorException)
def invalid_search_operator(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidSearchFieldException)
def invalid_search_field(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SearchNotFoundException)
def search_not_found(error):  # pragma: no cover
    return parse_exception(error)
