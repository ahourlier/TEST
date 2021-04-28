from typing import TypedDict


class AppConfigurationInterface(TypedDict, total=False):
    id: int
    key: str
    value: str
