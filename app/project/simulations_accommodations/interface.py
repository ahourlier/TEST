from mypy_extensions import TypedDict


class SimulationAccommodationInterface(TypedDict, total=False):
    id: int
    accommodation_id: int
    simulation_id: int
    rent_type: str
    rent_per_msq: float
    rent: float
