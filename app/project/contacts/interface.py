from mypy_extensions import TypedDict


class ContactInterface(TypedDict, total=False):
    id: int
    main_contact: bool
    email: str
    last_name: str
    first_name: str
    title: str
    phone_number: dict
    comment: str
    requester_id: int
