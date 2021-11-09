from .. import api
from .exceptions import MissionDetailNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(MissionDetailNotFoundException)
def mission_detail_not_found(error):  # pragma: no cover
    return parse_exception(error)
