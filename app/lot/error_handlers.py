from .controller import api
from .exceptions import LotNotFoundException
from ..common.error_handlers import parse_exception


@api.errorhandler(LotNotFoundException)
def lot_not_found(error):  # pragma: no cover
    return parse_exception(error)
