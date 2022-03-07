from . import api
from .exceptions import ReferentNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ReferentNotFoundException)
def referent_not_found(error):  # pragma: no cover
    return parse_exception(error)
