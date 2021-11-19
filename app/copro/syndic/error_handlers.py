from . import api
from .exceptions import SyndicNotFoundException, WrongSyndicTypeException
from ...common.error_handlers import parse_exception


@api.errorhandler(SyndicNotFoundException)
def syndic_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongSyndicTypeException)
def wrong_syndic_type(error):  # pragma: no cover
    return parse_exception(error)
