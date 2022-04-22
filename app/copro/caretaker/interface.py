from typing import Optional

from mypy_extensions import TypedDict


class CareTakerInterface(TypedDict):
    id: Optional[int]
    comment: Optional[str]
    phone_number: Optional[dict]
