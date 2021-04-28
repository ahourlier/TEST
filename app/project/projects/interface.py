from datetime import date

from mypy_extensions import TypedDict


class ProjectInterface(TypedDict, total=False):
    id: int
    status: str
    address: str
    type: str
    secondary_case_type: str
    work_type: str
    description: str
    closed: bool
    closure_motive: str
    urgent_visit: bool
    date_advice_meet: date
    date_control_advice: date
    notes: str
    mission_id: int
    requester_id: int
    accommodation_id: int
    active: bool
