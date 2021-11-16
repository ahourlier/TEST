from . import api
from .exceptions import SyndicNotFoundException, MissionNotTypeSyndicException
from ...common.error_handlers import parse_exception


@api.errorhandler(SyndicNotFoundException)
def syndic_not_found(error):  # pragma: no cover
    return parse_exception(error)

