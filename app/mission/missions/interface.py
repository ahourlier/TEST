from datetime import date
from typing import Optional, List

from mypy_extensions import TypedDict


class MissionInterface(TypedDict, total=False):
    id: int
    status: str
    name: str
    start_date: date
    end_date: date
    comment: str
    agency_id: int
    antenna_id: int
    client_id: int
    sdv2_operationel_drive: Optional[str]  # Mandatory for COPRO missions
    sdv2_administratif_drive: Optional[str]  # Mandatory for COPRO missions
    referents: Optional[List[dict]]
    managers: Optional[List[dict]]
