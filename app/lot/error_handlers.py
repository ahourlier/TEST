from .controller import api
from .exceptions import LotNotFoundException, IncorrectKeyException
from ..common.error_handlers import parse_exception


@api.errorhandler(LotNotFoundException)
def lot_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(IncorrectKeyException)
def incorrect_key(error):  # pragma: no cover
    return parse_exception(error)
