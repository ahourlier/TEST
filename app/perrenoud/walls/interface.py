from mypy_extensions import TypedDict


class WallInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    name: str
    wall_position: str
    insulated_heated_non_heated_wall: bool
    insulated_non_heated_exterior_wall: bool
    local_type: str
    known_U_value: bool
    known_U: float
    wall_composition: str
    double_brick_with_air_gap: bool
    insulated_wall: bool
    R_value: float
    insulation_thickness: int
    insulation_type: str
