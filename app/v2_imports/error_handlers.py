from . import api
from .exceptions import (
    MissionNotFoundException,
    ImportNotFoundException,
    LogSheetNotCreatedException,
    ImportStillRunningException,
    WrongImportTypeException
)
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(MissionNotFoundException)
def mission_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ImportNotFoundException)
def import_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(LogSheetNotCreatedException)
def log_sheet_not_created(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ImportStillRunningException)
def import_still_running(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongImportTypeException)
def wrong_import_type(error):  # pragma: no cover
    return parse_exception(error)
