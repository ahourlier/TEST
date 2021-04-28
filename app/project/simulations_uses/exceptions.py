from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION,
    SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION,
    SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION,
    KEY_SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION,
)


class SimulationDepositNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationPaymentRequestNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class SimulationCertifiedNotFoundException(HTTPException):
    def __init__(self, message=SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
