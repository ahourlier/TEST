from mypy_extensions import TypedDict


class DisorderInterface(TypedDict, total=False):
    id: int
    priority: int
    analysis_localisation: str
    analysis_comment: str
    recommendation_localisation: str
    recommendation_comment: str
    accommodation_id: int


class DisorderTypeInterface(TypedDict, total=False):
    id: int
    type_name: str
    is_analysis: bool
    disorder_id: int
