from mypy_extensions import TypedDict


class HotWaterInterface(TypedDict, total=False):
    id: int
    scenario_id: int
    name: str
    type: str
    boiler_type: str
    year_classic_accumulator: str
    has_light: bool
    production_living_volume: str
    linked_rooms: bool
    production_type: str
    water_tank_volume: int
    renovated_production: bool
    existing_solar_device: str
