from mypy_extensions import TypedDict


class FundingScenarioInterface(TypedDict, total=False):
    id: int
    criteria: dict
    rate: int
    upper_limit: int
    advance: int
    funder_id: int
