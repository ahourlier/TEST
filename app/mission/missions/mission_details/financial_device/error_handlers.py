from . import api
from .exceptions import FinancialDeviceNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(FinancialDeviceNotFoundException)
def financial_device_not_found(error):  # pragma: no cover
    return parse_exception(error)
