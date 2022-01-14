from . import api
from .exceptions import ElectNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ElectNotFoundException)
def partner_not_found(error):  # pragma: no cover
    return parse_exception(error)
