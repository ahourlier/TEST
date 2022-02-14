from mypy_extensions import TypedDict
from datetime import date


class MissionDetailInterface(TypedDict, total=False):
    id: int
    # general
    mission_id: int
    operational_plan: str
    job: str
    subjob: str
    previous_running_meeting: date
    # marche et facturation
    market_number: str
    os_signing_date: date
    has_sub_contractor: bool
    billing_type_tf: str
    billing_type_tc: str
    purchase_order_market: bool
    # smq
    smq_starting_meeting: date
    smq_engagement_meeting: date
    smq_previous_meeting: date