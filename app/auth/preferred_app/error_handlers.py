from . import api
from .exceptions import PreferredAppFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(PreferredAppFoundException)
def preferred_app_not_found(error):  # pragma: no cover
    return parse_exception(error)

