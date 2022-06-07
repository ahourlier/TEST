from typing import Optional

from mypy_extensions import TypedDict


class PersonInterface(TypedDict):
    id: Optional[int]
    civility: Optional[str]
    status: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    email_address: Optional[str]
    antenna_id: Optional[int]
    antenna: Optional[dict]
    phone_number: Optional[dict]
    is_physical_person: Optional[bool]
