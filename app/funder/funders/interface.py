from mypy_extensions import TypedDict


class FunderInterface(TypedDict, total=False):
    id: int
    name: str
    subvention_round: int
    type: int
    is_national: bool
    mission_id: int
    position: int
