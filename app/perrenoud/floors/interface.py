from mypy_extensions import TypedDict


class FloorInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    name: str
    position: str
    perimeter: float
    insulated_heated_non_heated_wall: bool
    insulated_non_heated_exterior_wall: bool
    type_non_heated_local: str
    known_U_value: bool
    U_value: float
    main_component: str
    insulated_wall: bool
    known_insulation_value: str
    R_value: float
    insulation_thickness: int
    insulation_type: str
