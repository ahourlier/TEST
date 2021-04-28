from . import api
from .exceptions import ContactNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ContactNotFoundException)
def contact_not_found(error):  # pragma: no cover
    return parse_exception(error)
