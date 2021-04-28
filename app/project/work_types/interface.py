from mypy_extensions import TypedDict


class WorkTypeInterface(TypedDict, total=False):
    id: int
    type_name: str
    project_id: int
