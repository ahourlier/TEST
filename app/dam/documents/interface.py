from mypy_extensions import TypedDict


class DocumentInterface(TypedDict, total=False):
    id: int
    name: str
    template_id: str
    document_id: str
    project_id: int
    user_id: int
    status: str
    source: str
