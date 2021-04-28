from datetime import date
from mypy_extensions import TypedDict


class TaxableIncomeInterface(TypedDict, total=False):
    id: int
    date: date
    income: int
    requester_id: int
