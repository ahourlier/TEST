from mypy_extensions import TypedDict


class ClientInterface(TypedDict, total=False):
    id: int
    name: str
    postal_address: str
    title: str
    last_name: str
    first_name: str
    job_function: str
    phone_number: dict
    email_address: str
    comment: str
