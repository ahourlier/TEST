from mypy_extensions import TypedDict


class CommentInterface(TypedDict, total=False):
    id: int
    content: str
    html_content: str
    project_id: int
    author_id: int
