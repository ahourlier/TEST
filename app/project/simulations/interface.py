from datetime import datetime
from typing import Optional

from mypy_extensions import TypedDict


class SimulationInterface(TypedDict, total=False):
    id: int
    name: str
    project_id: int
    quotes_modified: bool
    note_certifications: str
    note_payment_requests: str
    note_deposits: str
    scenario_id: Optional[int]


class SimulationQuoteInterface(TypedDict, total=False):
    id: int
    modification_date: datetime
    base_quote_id: int
    duplicate_quote_id: int
    simulation_id: int


class SimulationFunderInterface(TypedDict, total=False):
    id: int
    base_funder_id: int
    simulation_funder_id: int
    simulation_id: int


class SimulationUseCaseInterface(TypedDict, total=False):
    id: int
    use_case_name: str
    simulation_id: int
