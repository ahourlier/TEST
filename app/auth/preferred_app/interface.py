from mypy_extensions import TypedDict


class PreferredAppInterface(TypedDict, total=False):
    preferred_app: str
    first_connection: bool
