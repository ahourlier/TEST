from mypy_extensions import TypedDict


class HistoricInterface(TypedDict, total=False):
    id: int
    thematique_id: str
    old_value: dict
    new_value: dict
