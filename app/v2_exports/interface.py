from typing import Optional
from datetime import date
from mypy_extensions import TypedDict


class ExportInterface(TypedDict):
    id: int
    mission_id: int
    name: str
    status: Optional[str]
    type: Optional[str]
    author_id: Optional[int]
