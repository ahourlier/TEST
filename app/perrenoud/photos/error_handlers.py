from . import api
from .exceptions import (
    PhotoNotFoundException,
    MissingPhotoException,
    MissingNameException,
    MissingSectionException,
    MissingRoomException,
    InvalidPhotoContextException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(PhotoNotFoundException)
def photo_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingPhotoException)
def missing_photo(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingNameException)
def missing_name(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingSectionException)
def missing_section(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingRoomException)
def missing_room(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidPhotoContextException)
def invalid_photo_context_exception(error):  # pragma: no cover
    return parse_exception(error)
