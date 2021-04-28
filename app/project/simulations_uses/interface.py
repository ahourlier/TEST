from datetime import date

from mypy_extensions import TypedDict


class SimulationDepositInterface(TypedDict, total=False):
    id: int
    deposit_date: date
    funder_id: int
    simulation_id: int


class SimulationPaymentRequestInterface(TypedDict, total=False):
    id: int
    payment_request_date: date
    funder_id: int
    simulation_id: int


class SimulationCertifiedInterface(TypedDict, total=False):
    id: int
    certification_date: date
    funder_id: int
    simulation_id: int
