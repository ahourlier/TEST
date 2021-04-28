from mypy_extensions import TypedDict


class MonitorInterface(TypedDict, total=False):
    id: int
    mission_id: int
    advance_alert: int
    payment_alert: int


class MonitorFieldInterface(TypedDict, total=False):
    id: int
    monitor_id: int
    type: str
    name: str
    invisible: bool
    default: bool
    automatic: bool
