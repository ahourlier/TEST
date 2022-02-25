from .controller import api
from .exceptions import (
    MissionNotFoundException,
    ImportNotFoundException
)
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(MissionNotFoundException)
def mission_not_found(error):  # pragma: no cover
    return parse_exception(error)

@api.errorhandler(ImportNotFoundException)
def import_not_found(error):  # pragma: no cover
    return parse_exception(error)
