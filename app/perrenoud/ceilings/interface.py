from mypy_extensions import TypedDict


class CeilingInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    name: str
    known_U_value: bool
    U_value: float
    composition: str
    insulated_wall: bool
    known_insulation_value: bool
    R_value: float
    insulation_thickness: int
    insulation_type: str
    ceiling_position: str
    insulated_heated_non_heated_wall: bool
    insulated_non_heated_exterior_wall: bool
    type_non_heated_local: str
