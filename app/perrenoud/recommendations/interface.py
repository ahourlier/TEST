from mypy_extensions import TypedDict


class RecommendationInterface(TypedDict, total=False):

    id: int
    recommendation: str
    scenario_id: int
    heating_id: int
    hot_water_id: int
    wall_id: int
