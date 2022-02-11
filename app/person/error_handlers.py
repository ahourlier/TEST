from . import api
from .exceptions import PersonNotFoundException
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(PersonNotFoundException)
def person_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(EnumException)
def enum_exception(error):  # pragma: no cover
    return parse_exception(error)
