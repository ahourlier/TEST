from . import api
from .exceptions import PartnerNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(PartnerNotFoundException)
def partner_not_found(error):  # pragma: no cover
    return parse_exception(error)
