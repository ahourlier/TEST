from . import api
from .exceptions import RequesterNotFoundException, RequesterTypeConstantException
from app.common.error_handlers import parse_exception


@api.errorhandler(RequesterNotFoundException)
def requester_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(RequesterTypeConstantException)
def requester_type_constant(error):  # pragma: no cover
    return parse_exception(error)
