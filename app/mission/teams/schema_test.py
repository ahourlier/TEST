from pytest import fixture

from .model import Team
from .test.fixtures import TEAM_ONE_USER_POSITION
from .schema import TeamSchema


@fixture
def schema() -> TeamSchema:
    return TeamSchema()


def test_team_schema_create(schema: TeamSchema):
    assert schema


def test_team_schema_ok(schema: TeamSchema):
    params = schema.load(
        {
            "user_position": TEAM_ONE_USER_POSITION,
            "mission_id": 1,
            "user_id": 1,
        }
    )

    team = Team(**params)

    assert team.user_position == TEAM_ONE_USER_POSITION
    assert team.user_id == 1
    assert team.mission_id == 1
