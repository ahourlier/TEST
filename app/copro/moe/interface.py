from typing import Optional

from mypy_extensions import TypedDict


class MoeInterface(TypedDict):
    id: Optional[int]
    name: Optional[str]
    email_address: Optional[str]
    comment: Optional[str]
    address_id: Optional[int]
    address: Optional[dict]
    phone_number: Optional[dict]
