from mypy_extensions import TypedDict


class UserInterface(TypedDict, total=False):
    id: int
    uid: str
    email: str
    last_name: str
    first_name: str
    comment: str
    role: str
    kind: str
    active: bool
