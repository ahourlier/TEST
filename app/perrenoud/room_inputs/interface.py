from mypy_extensions import TypedDict


class RoomInputInterface(TypedDict, total=False):
    id: int
    kind: str
    room_id: int
    wall_id: int
    woodwork_id: int
    ceiling_id: int
    floor_id: int
    thermal_bridge_id: int
    number_identical_woodwork: int
