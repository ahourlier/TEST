from mypy_extensions import TypedDict


class ScenarioInterface(TypedDict, total=False):

    id: int
    is_initial_state: bool
    name: str
    accommodation_id: int
    annual_energy_consumption: float
    energy_label: str
    energy_gain: int
    annual_GES_emission: float
    GES_label: str
    loss_upper_limit: int
    loss_exterior_wall: int
    loss_local_wall: int
    loss_floor: int
    loss_windows: int
    loss_doors: int
    loss_heat_bridges: int
    loss_airflow: int
    heat_energy_1_final: float
    heat_energy_1_primary: float
    heat_energy_2_final: float
    heat_energy_2_primary: float
    ECS_energy_1_final: float
    ECS_energy_1_primary: float
    ECS_energy_2_final: float
    ECS_energy_2_primary: float
    cooling_energy_1_final: float
    cooling_energy_1_primary: float
    airflow_device: str
    air_conditioning_type: str
    air_conditioned_area: float
    has_photovoltaic_device: bool
    photovoltaic_device_surface: float
    living_area: float
    average_height: float
    inertia: str
    altitude: str
