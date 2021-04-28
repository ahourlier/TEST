from mypy_extensions import TypedDict


class WoodworkInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    door_name: str
    windows_name: str
    type_election: str
    woodwork_known_U_value: bool
    woodwork_U_value: float
    door_nature: str
    door_type: str
    door_known_U_value: bool
    door_U_value: float
    Ujn_value: float
    glass_wall_type: str
    windows_type: str
    materials: str
    glass_type: str
    glass_insulated: bool
    argon_krypton_filling: bool
    thickness_air_gap: int
    closing_type: str
    inclination: str
