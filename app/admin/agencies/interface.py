from mypy_extensions import TypedDict


class AgencyInterface(TypedDict, total=False):
    id: int
    name: str
    postal_address: str
    email_address: str
