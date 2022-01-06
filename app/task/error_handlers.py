from .controller import api
from .exceptions import TaskNotFoundException
from ..common.error_handlers import parse_exception


@api.errorhandler(TaskNotFoundException)
def task_not_found(error):  # pragma: no cover
    return parse_exception(error)
