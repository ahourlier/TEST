from .indicators import api
from app.common.exceptions import InvalidSearchFieldException
from app.common.error_handlers import parse_exception


@api.errorhandler(InvalidSearchFieldException)
def invalid_search_field(error):  # pragma: no cover
    return parse_exception(error)
