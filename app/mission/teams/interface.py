from typing import List

from mypy_extensions import TypedDict


class TeamInterface(TypedDict, total=False):
    id: int
    user_position: str
    mission_id: int
    user_id: int


class TeamListInterface(TypedDict, total=False):
    mission_id: int
    mission_managers: List[int]
    collaborators: List[int]
    external_collaborators: List[int]
    users_additional_access: List[int]
    agencies_additional_access: List[int]
    antennas_additional_access: List[int]
