from mypy_extensions import TypedDict


class ProjectLeadInterface(TypedDict, total=False):
    id: int
    project_id: int
    user_id: int
