from . import api
from .exceptions import PreferredAppNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(PreferredAppNotFoundException)
def preferred_app_not_found(error):  # pragma: no cover
    return parse_exception(error)

