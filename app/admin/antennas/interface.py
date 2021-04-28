from mypy_extensions import TypedDict


class AntennaInterface(TypedDict, total=False):
    id: int
    name: str
    postal_address: str
    email_address: str
    agency_id: int
