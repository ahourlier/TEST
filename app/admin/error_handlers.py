from .agencies import api
from app.common.exceptions import InconsistentUpdateIdException, ChildMissionException
from app.common.error_handlers import parse_exception


@api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ChildMissionException)
def child_mission_exception(error):  # pragma: no cover
    return parse_exception(error)
