from . import api
from .exceptions import WorkTypeNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(WorkTypeNotFoundException)
def work_type_not_found(error):  # pragma: no cover
    return parse_exception(error)
