from datetime import date

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
