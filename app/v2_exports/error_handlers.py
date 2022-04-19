from . import api
from .exceptions import (
    MissionNotFoundException,
    ExportNotFoundException,
    LogSheetNotCreatedException,
)
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(MissionNotFoundException)
def mission_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ExportNotFoundException)
def export_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(LogSheetNotCreatedException)
def log_sheet_not_created(error):  # pragma: no cover
    return parse_exception(error)