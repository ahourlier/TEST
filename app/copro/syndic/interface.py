from typing import List, Optional
from datetime import date
from mypy_extensions import TypedDict


class SyndicInterface(TypedDict, total=False):
    id: Optional[int]
    copro_id: Optional[int]
    copro: Optional[dict]
    name: Optional[str]
    type: Optional[str]
    manager_name: Optional[str]
    manager_address_id: Optional[int]
    manager_address: Optional[dict]
    manager_email: Optional[str]
    comment: Optional[str]
