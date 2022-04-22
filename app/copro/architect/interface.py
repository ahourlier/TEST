from typing import Optional

from mypy_extensions import TypedDict


class ArchitectInterface(TypedDict):
    id: Optional[int]
    qualification: Optional[str]
    name: Optional[str]
    email_address: Optional[str]
    comment: Optional[str]
    address_id: Optional[int]
    address: Optional[dict]
    phone_number: Optional[dict]
