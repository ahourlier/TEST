from . import api
from .exceptions import (
    RoomInputNotFoundException,
    InvalidRoomInputKindException,
    TypeRoomInputInUseException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(RoomInputNotFoundException)
def room_input_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidRoomInputKindException)
def invalid_room_input_kind(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(TypeRoomInputInUseException)
def type_room_input_in_use(error):  # pragma: no cover
    return parse_exception(error)
