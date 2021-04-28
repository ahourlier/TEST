from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    PHOTO_NOT_FOUND_EXCEPTION,
    KEY_PHOTO_NOT_FOUND_EXCEPTION,
    MISSING_PHOTO_EXCEPTION,
    KEY_MISSING_PHOTO_EXCEPTION,
    MISSING_NAME_EXCEPTION,
    KEY_MISSING_NAME_EXCEPTION,
    MISSING_SECTION_EXCEPTION,
    KEY_MISSING_SECTION_EXCEPTION,
    MISSING_ROOM_EXCEPTION,
    KEY_MISSING_ROOM_EXCEPTION,
    INVALID_PHOTO_CONTEXT_EXCEPTION,
    KEY_INVALID_PHOTO_CONTEXT_EXCEPTION,
)


class PhotoNotFoundException(HTTPException):
    def __init__(self, message=PHOTO_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_PHOTO_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class MissingPhotoException(HTTPException):
    def __init__(self, message=MISSING_PHOTO_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_PHOTO_EXCEPTION
        self.message = message
        self.status = "BAD_REQUEST"


class MissingNameException(HTTPException):
    def __init__(self, message=MISSING_NAME_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_NAME_EXCEPTION
        self.message = message
        self.status = "BAD_REQUEST"


class MissingSectionException(HTTPException):
    def __init__(self, message=MISSING_SECTION_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_SECTION_EXCEPTION
        self.message = message
        self.status = "BAD_REQUEST"


class MissingRoomException(HTTPException):
    def __init__(self, message=MISSING_ROOM_EXCEPTION):
        self.code = 400
        self.key = KEY_MISSING_ROOM_EXCEPTION
        self.message = message
        self.status = "BAD_REQUEST"


class InvalidPhotoContextException(HTTPException):
    def __init__(self, message=INVALID_PHOTO_CONTEXT_EXCEPTION):
        self.code = 400
        self.key = KEY_INVALID_PHOTO_CONTEXT_EXCEPTION
        self.message = message
        self.status = "BAD_REQUEST"
