from . import api
from .exceptions import RoomNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(RoomNotFoundException)
def room_not_found(error):  # pragma: no cover
    return parse_exception(error)
