from . import api
from .exceptions import TeamNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(TeamNotFoundException)
def team_not_found(error):  # pragma: no cover
    return parse_exception(error)
