from . import api
from .exceptions import (
    MonitorNotFoundException,
    MonitorFieldNotFoundException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(MonitorNotFoundException)
def monitor_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(MonitorFieldNotFoundException)
def monitor_field_not_found(error):  # pragma: no cover
    return parse_exception(error)
