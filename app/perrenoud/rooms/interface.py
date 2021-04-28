from mypy_extensions import TypedDict


class RoomInterface(TypedDict, total=False):

    id: int
    name: str
    scenario_id: int
    heating_id: int
    height_under_ceiling: float
    air_conditioning: bool
