from .controller import api
from .exceptions import TaskNotFoundException, BadFormatAssigneeException, InvalidTaskType
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(TaskNotFoundException)
def task_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(BadFormatAssigneeException)
def assignee_bad_format(error):  # pragma: no cover
    return parse_exception(error)

@api.errorhandler(InvalidTaskType)
def invalid_task_type(error):  # pragma: no cover
    return parse_exception(error)

@api.errorhandler(EnumException)
def enum_exception(error):  # pragma: no cover
    return parse_exception(error)
