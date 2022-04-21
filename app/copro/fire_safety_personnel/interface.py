from typing import Optional

from mypy_extensions import TypedDict


class FireSafetyPersonnelInterface(TypedDict):
    id: Optional[int]
    comment: Optional[str]
    phone_number: Optional[dict]
