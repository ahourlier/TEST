from mypy_extensions import TypedDict


class ProjectCustomFieldInterface(TypedDict, total=False):
    id: int
    custom_field_id: int
    project_id: int
    value: str


class CustomFieldValueInterface(TypedDict, total=False):
    id: int
    project_custom_field_id: int
    value: str
