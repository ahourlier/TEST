from . import api
from .exceptions import MissionNotFoundException
from app.common.error_handlers import parse_exception
from app.common.exceptions import SharedDriveException, GoogleGroupsException


@api.errorhandler(MissionNotFoundException)
def mission_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SharedDriveException)
def shared_drive_exception(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(GoogleGroupsException)
def google_groups_exception(error):  # pragma: no cover
    return parse_exception(error)
