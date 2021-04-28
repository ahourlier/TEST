from . import api
from .exceptions import (
    AntennaNotFoundException,
    AntennaDuplicateNameException,
    ChildAntennaMissionException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(AntennaNotFoundException)
def antenna_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(AntennaDuplicateNameException)
def antenna_duplicate_name(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ChildAntennaMissionException)
def child_antenna_mission(error):  # pragma: no cover
    return parse_exception(error)
