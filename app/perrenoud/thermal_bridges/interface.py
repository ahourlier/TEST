from mypy_extensions import TypedDict


class ThermalBridgeInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    type: str
    length_m_liaison: float
    wall_name: str
    floor_name: str
    ceiling_name: str
    position_medium_floor: str
    position_shear_wall: str
