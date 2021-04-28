from . import api
from app.common.error_handlers import parse_exception
from .exceptions import FunderMonitoringValueNotFoundException


@api.errorhandler(FunderMonitoringValueNotFoundException)
def funder_monitoring_value_not_found(error):  # pragma: no cover
    return parse_exception(error)
