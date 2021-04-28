from . import api
from .exceptions import (
    ScenarioNotFoundException,
    InitialStateAlreadyCreatedException,
    PerrenoudWebserviceException,
    MissingPerrenoudDataException,
)
import logging
from app.common.error_handlers import parse_exception
from ...common.exceptions import XMLGenerationException


@api.errorhandler(ScenarioNotFoundException)
def scenario_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InitialStateAlreadyCreatedException)
def initial_state_already_created(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(XMLGenerationException)
def xm_generation_error(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(PerrenoudWebserviceException)
def xm_generation_error(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MissingPerrenoudDataException)
def missing_perrenoud_data(error):  # pragma: no cover
    logging.error(error.message)
    return (
        {
            "key": error.key,
            "status": error.status,
            "scenario_name": error.scenario_name,
            "is_initial_state": error.is_initial_state,
            "message": error.message,
            "errors_count": error.errors_count,
            "errors": error.errors,
        },
        error.code,
    )
