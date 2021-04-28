from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    ROOM_INPUT_NOT_FOUND_EXCEPTION,
    KEY_ROOM_INPUT_NOT_FOUND_EXCEPTION,
    INVALID_ROOM_INPUT_KIND_EXCEPTION,
    KEY_INVALID_ROOM_INPUT_KIND_EXCEPTION,
    TYPE_ROOM_INPUT_IN_USE_EXCEPTION,
    KEY_TYPE_ROOM_INPUT_IN_USE_EXCEPTION,
)


class RoomInputNotFoundException(HTTPException):
    def __init__(self, message=ROOM_INPUT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_ROOM_INPUT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class InvalidRoomInputKindException(HTTPException):
    def __init__(self, message=INVALID_ROOM_INPUT_KIND_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_ROOM_INPUT_KIND_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class TypeRoomInputInUseException(HTTPException):
    def __init__(self, message=TYPE_ROOM_INPUT_IN_USE_EXCEPTION):
        self.code = 400
        self.key = KEY_TYPE_ROOM_INPUT_IN_USE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
