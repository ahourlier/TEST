from .controller import api
from .exceptions import (
    StepOrVersionMissingException,
    TaskNotFoundException,
    BadFormatAssigneeException,
    InvalidTaskTypeException,
)
from ..common.error_handlers import parse_exception
from ..common.exceptions import EnumException


@api.errorhandler(TaskNotFoundException)
def task_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(BadFormatAssigneeException)
def assignee_bad_format(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidTaskTypeException)
def invalid_task_type(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(EnumException)
def enum_exception(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(StepOrVersionMissingException)
def step_version_missing(error):  # pragma: no cover
    return parse_exception(error)
