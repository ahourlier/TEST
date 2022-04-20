from mypy_extensions import TypedDict


class HistoricInterface(TypedDict, total=False):
    id: int
    version_id: str
    updated_by: str
    status_changed: bool
    old_status: str
    new_status: str
