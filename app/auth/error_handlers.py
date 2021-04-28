from .users import api
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidSearchFieldException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidSearchFieldException)
def invalid_search_field(error):  # pragma: no cover
    return parse_exception(error)
