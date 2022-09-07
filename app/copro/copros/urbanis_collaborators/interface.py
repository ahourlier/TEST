from typing import Optional
from mypy_extensions import TypedDict


class UrbanisCollaboratorsInterface(TypedDict):
    id: Optional[int]
    user_in_charge_id: Optional[int]
    copro_id: Optional[int]
