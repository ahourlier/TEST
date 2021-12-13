from .controller import api
from .exceptions import (
    VersionNotFoundException,
    InvalidScopeException,
    InvalidResourceIdException,
    InvalidThematiqueNameException, MissingVersionIdException, MissingStepIdException,
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
