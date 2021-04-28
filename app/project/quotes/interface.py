from mypy_extensions import TypedDict


class QuoteInterface(TypedDict, total=False):
    id: int
    is_bill: bool
    name: str
    company: str
    precision: str
    price_excl_tax: float
    price_incl_tax: float
    eligible_amount: float
    note: str
    project_id: int


class QuoteWorkTypeInterface(TypedDict, total=False):
    id: int
    type_name: str
    quote_id: int
