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
    financial_device_used: date
    mandate_account_type: str
    organization_funds_provider: str
    bank_account_name: str
    bank_name: str
    agreement_signature_date: date
    amendment_signature_date: date
    convention_number: str
    initiale_envelop: int
    complementary_envelop: int
    internal_audit_date: date
    external_audit_date: date
    funds_return_date: date
    amount_returned: int
    closing_date: date
    transfer_circuit_validation: str
    operating_details: str
    # smq
    smq_starting_meeting: date
    smq_engagement_meeting: date
    smq_previous_meeting: date
    smq_meeting_progress_1: date
    smq_meeting_progress_2: date
    smq_meeting_progress_3: date
    smq_meeting_progress_4: date
    smq_meeting_progress_5: date
    smq_meeting_cloture: date
    smq_internal_audit_date: date
    smq_external_audit_date: date
    sqm_commentary: str
