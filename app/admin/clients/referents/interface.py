from mypy_extensions import TypedDict


class ReferentInterface(TypedDict, total=False):
    id: int
    first_name = str
    last_name = str
    email = str
    phone_number: dict
    mission_id: int
    function = str
