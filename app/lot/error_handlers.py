from . import api
from .exceptions import LotNotFoundException, IncorrectKeyException
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(LotNotFoundException)
def lot_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(IncorrectKeyException)
def incorrect_key(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(EnumException)
def enum_exception(error):  # pragma: no cover
    return parse_exception(error)
