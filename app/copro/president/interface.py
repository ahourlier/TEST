from datetime import date
from typing import Optional

from mypy_extensions import TypedDict


class PresidentInterface(TypedDict, total=False):
    id: Optional[int]
    copro_id: Optional[int]
    copro: Optional[dict]
    name: Optional[str]
    email_address: Optional[str]
    election_date: Optional[date]
    phone_number: Optional[dict]
