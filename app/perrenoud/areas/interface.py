from mypy_extensions import TypedDict


class AreaInterface(TypedDict, total=False):
    id: int
    room_id: int
    room_input_id: int
    length: float
    width: float
    height: float
    wall_id: int
    ceiling_id: int
    number_identical_woodwork: int
