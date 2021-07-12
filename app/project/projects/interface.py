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
    date_asking_for_pay: date
    date_build_on_going: date
    date_certified: date
    date_cleared: date
    date_contact: date
    date_control_meet: date
    date_depositted: date
    date_dismissed: date
    date_meet_advices_planned: date
    date_meet_advices_to_plan: date
    date_meet_control_planned: date
    date_meet_control_to_plan: date
    date_meet_to_process: date
    date_non_eligible: date
    date_payment_request_to_do: date
    date_to_contact: date
    notes: str
    mission_id: int
    requester_id: int
    accommodation_id: int
    active: bool
