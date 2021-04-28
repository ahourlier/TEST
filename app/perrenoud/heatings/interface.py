from mypy_extensions import TypedDict


class HeatingInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    heating_name: str
    emissions_type: str
    energy_used: str
    generator_type: str
    is_power_known: bool
    power: int
    has_regulation: bool
    wall_mounted_boiler: bool
    isolated_network: bool
    emettor_type: str
    installation_year: str
    intermittent_equipment: str
    wood_oven: bool
    equipment_performance: str
    heated_area: float
    known_caracteristics: bool
    full_yield: float
    middle_yield: float
    COP: float
