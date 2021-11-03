from typing import Optional

from mypy_extensions import TypedDict


class ReferentInterface(TypedDict, total=False):
    id: int
    first_name = str
    last_name = str
    email = Optional[str]
    phone_number: Optional[dict]
    mission_id: int
    function = str
