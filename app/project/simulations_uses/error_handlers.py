from . import api
from app.common.error_handlers import parse_exception
from .exceptions import (
    SimulationDepositNotFoundException,
    SimulationPaymentRequestNotFoundException,
    SimulationCertifiedNotFoundException,
)


@api.errorhandler(SimulationDepositNotFoundException)
def simulation_deposit_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationPaymentRequestNotFoundException)
def simulation_payment_request_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(SimulationCertifiedNotFoundException)
def simulation_certified_not_found(error):  # pragma: no cover
    return parse_exception(error)
