from datetime import date

from mypy_extensions import TypedDict


class FunderMonitoringValueInterface(TypedDict, total=False):
    id: int
    project_id: int
    funder_id: int
    monitor_field_id: int
    date_value: date
    boolean_value: bool
