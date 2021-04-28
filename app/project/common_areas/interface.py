from datetime import date
from mypy_extensions import TypedDict


class CommonAreaInterface(TypedDict, total=False):
    id: int
    condominium: bool
    purchase_year: date
    construction_year: date
    levels_nb: int
    commentary: str
    accommodations_nb: int
    project_id: int
