from mypy_extensions import TypedDict


class CustomFieldInterface(TypedDict, total=False):
    id: int
    mission_id: int
    name: str
    category: str
    type: str
    is_multiple: bool


class AvailableFieldValueInterface(TypedDict, total=False):
    id: int
    custom_field_id: int
    value: str
