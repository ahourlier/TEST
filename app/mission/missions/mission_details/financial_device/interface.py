from typing import Optional
from datetime import date

class FinancialDeviceInterface:
    
    mandate_account_type: Optional[str]
    organization_funds_provider: Optional[str]
    bank_account_name: Optional[str]
    bank_name: Optional[str]
    agreement_signature_date: Optional[date]
    amendment_signature_date: Optional[date]
    convention_number: Optional[str]
    initiale_envelop: Optional[int]
    complementary_envelop: Optional[int]
    internal_audit_date: Optional[date]
    external_audit_date: Optional[date]
    funds_return_date: Optional[date]
    amount_returned: Optional[int]
    closing_date: Optional[date]
    transfer_circuit_validation: Optional[str]
    operating_details: Optional[str]