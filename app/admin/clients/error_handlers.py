from . import api
from .exceptions import ClientNotFoundException, ChildClientMissionException
from app.common.error_handlers import parse_exception


@api.errorhandler(ClientNotFoundException)
def client_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ChildClientMissionException)
def child_client_mission(error):  # pragma: no cover
    return parse_exception(error)
