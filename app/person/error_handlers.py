from .controller import api
from .exceptions import PersonNotFoundException
from ..common.error_handlers import parse_exception


@api.errorhandler(PersonNotFoundException)
def person_not_found(error):  # pragma: no cover
    return parse_exception(error)
