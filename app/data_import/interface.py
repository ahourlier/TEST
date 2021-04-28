from mypy_extensions import TypedDict


class DataImportInterface(TypedDict, total=False):
    id: int
    status: str
    user_email: str
    data: str
    labels: str
