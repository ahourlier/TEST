from mypy_extensions import TypedDict


class SearchInterface(TypedDict, total=False):
    id: int
    name: str
    is_favorite: bool
    search: str
    user_id: id
