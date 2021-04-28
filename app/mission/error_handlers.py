from .missions import api
from app.common.exceptions import InconsistentUpdateIdException
from app.common.error_handlers import parse_exception


@api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)
