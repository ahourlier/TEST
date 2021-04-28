from . import api
from .exceptions import (
    AgencyNotFoundException,
    ChildAntennaException,
    AgencyDuplicateNameException,
    ChildAgencyMissionException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(AgencyNotFoundException)
def agency_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ChildAntennaException)
def child_antenna(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ChildAgencyMissionException)
def child_antenna_mission(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(AgencyDuplicateNameException)
def agency_duplicate_name(error):
    return parse_exception(error)
