from . import api
from .exceptions import (
    CoproNotFoundException,
    MissionNotTypeCoproException,
    RepartitionKeyLinkedException,
)
from ...common.error_handlers import parse_exception


@api.errorhandler(CoproNotFoundException)
def copro_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissionNotTypeCoproException)
def wrong_mission_type(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(RepartitionKeyLinkedException)
def repartition_key_linked(error):  # pragma: no cover
    return parse_exception(error)
