from typing import Optional
from datetime import date
from mypy_extensions import TypedDict


class ImportInterface(TypedDict):
    id: int
    mission_id: int
    import_sheet_id: str
    import_type: str
    name: str
    log_sheet_id: Optional[str]
    status: Optional[str]
    type: Optional[str]
