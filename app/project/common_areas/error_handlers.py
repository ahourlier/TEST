from . import api
from .exceptions import ExistingCommonAreaException, CommonAreaNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ExistingCommonAreaException)
def existing_common_area(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(CommonAreaNotFoundException)
def common_area_not_found(error):  # pragma: no cover
    return parse_exception(error)
