from pytest import fixture

from .model import Mission
from .interface import MissionInterface
from .test.fixtures import (
    MISSION_STATUS_ONE,
    MISSION_NAME_ONE,
    MISSION_START_DATE_ONE,
    MISSION_END_DATE_ONE,
    MISSION_COMMENT_ONE,
)


def get_mission_one_interface() -> MissionInterface:
    return MissionInterface(
        status=MISSION_STATUS_ONE,
        name=MISSION_NAME_ONE,
        start_date=MISSION_START_DATE_ONE,
        end_date=MISSION_END_DATE_ONE,
        comment=MISSION_COMMENT_ONE,
        agency_id=1,
        antenna_id=1,
        client_id=1,
    )


@fixture
def interface() -> MissionInterface:
    return get_mission_one_interface()


def test_mission_interface_create(interface: MissionInterface):
    assert interface


def test_mission_interface_ok(interface: MissionInterface):
    mission = Mission(**interface)
    assert mission
