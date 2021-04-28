from pytest import fixture

from .model import Mission
from .test.fixtures import (
    MISSION_STATUS_ONE,
    MISSION_NAME_ONE,
    MISSION_COMMENT_ONE,
    MISSION_START_DATE_ONE,
    MISSION_END_DATE_ONE,
)
from .schema import MissionSchema
from ...common.constants import DATE_FORMAT


@fixture
def schema() -> MissionSchema:
    return MissionSchema()


def test_mission_schema_create(schema: MissionSchema):
    assert schema


def test_mission_schema_ok(schema: MissionSchema):
    params = schema.load(
        {
            "status": MISSION_STATUS_ONE,
            "name": MISSION_NAME_ONE,
            "comment": MISSION_COMMENT_ONE,
            "start_date": MISSION_START_DATE_ONE.strftime(DATE_FORMAT),
            "end_date": MISSION_END_DATE_ONE.strftime(DATE_FORMAT),
            "agency_id": 1,
            "antenna_id": 1,
            "client_id": 1,
        }
    )

    mission = Mission(**params)

    assert mission.status == MISSION_STATUS_ONE
    assert mission.name == MISSION_NAME_ONE
    assert mission.comment == MISSION_COMMENT_ONE
    assert mission.start_date == MISSION_START_DATE_ONE
    assert mission.end_date == MISSION_END_DATE_ONE
    assert mission.agency_id == 1
    assert mission.antenna_id == 1
    assert mission.client_id == 1
