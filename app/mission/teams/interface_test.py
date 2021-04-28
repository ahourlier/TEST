from pytest import fixture

from .model import Team
from .interface import TeamInterface
from .test.fixtures import TEAM_ONE_USER_POSITION


def get_team_one_interface(mission_id: int = 1, user_id: int = 1) -> TeamInterface:
    return TeamInterface(
        user_position=TEAM_ONE_USER_POSITION, mission_id=mission_id, user_id=user_id
    )


@fixture
def interface() -> TeamInterface:
    return get_team_one_interface()


def test_team_interface_create(interface: TeamInterface):
    assert interface


def test_team_interface_ok(interface: TeamInterface):
    team = Team(**interface)
    assert team
