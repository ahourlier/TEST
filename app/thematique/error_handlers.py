from . import api
from .exceptions import (
    VersionNotFoundException,
    InvalidScopeException,
    InvalidResourceIdException,
    InvalidThematiqueNameException,
    MissingVersionIdException,
    MissingStepIdException,
    StepNotFoundException,
    UnauthorizedToDeleteException,
    UnauthorizedToUpdateException,
    UnauthorizedDuplicationException,
    NotUniqueDataAndNameVersionException,
)
from ..common.error_handlers import parse_exception


@api.errorhandler(VersionNotFoundException)
def version_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidScopeException)
def invalid_scope(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidResourceIdException)
def invalid_resource_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InvalidThematiqueNameException)
def invalid_thematique_name(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingVersionIdException)
def missing_version_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingStepIdException)
def missing_step_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(StepNotFoundException)
def step_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UnauthorizedToDeleteException)
def deletion_unauthorized(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UnauthorizedToUpdateException)
def update_unauthorized(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UnauthorizedDuplicationException)
def duplication_unauthorized(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(NotUniqueDataAndNameVersionException)
def not_unique_date_and_name_version(error):  # pragma: no cover
    return parse_exception(error)
