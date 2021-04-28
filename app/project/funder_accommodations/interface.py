from mypy_extensions import TypedDict


class FunderAccommodationInterface(TypedDict, total=False):
    id: int
    simulation_accommodation_id: int
    simulation_funder_id: int
    is_common_area: bool
    rate: int
    subventioned_expense: int
