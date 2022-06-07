from . import api

from .exceptions import CreateHistoricException, HistoricNotFoundException

from app.common.error_handlers import parse_exception


@api.errorhandler(CreateHistoricException)
def create_historic_failed(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(HistoricNotFoundException)
def historic_not_found(error):  # pragma: no cover
    return parse_exception(error)
