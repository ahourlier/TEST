from . import api
from .exceptions import CoproNotFoundException, MissionNotTypeCoproException, WrongCoproTypeException, \
    WrongConstructionTimeException
from ...common.error_handlers import parse_exception


@api.errorhandler(CoproNotFoundException)
def copro_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissionNotTypeCoproException)
def wrong_mission_type(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongCoproTypeException)
def wrong_copro_type(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongConstructionTimeException)
def wrong_construction_time(error):  # pragma: no cover
    return parse_exception(error)
