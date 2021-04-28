import datetime

from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.admin.agencies import Agency
from app.admin.antennas import Antenna
from app.admin.clients import Client
from app.mission.missions import Mission
from app.mission.missions.model import MissionStatus

# FIXTURES IMPORT
from app.admin.agencies.model_test import agency
from app.admin.antennas.model_test import antenna, create_antenna_one
from app.admin.clients.model_test import client


MISSION_STATUS_ONE = MissionStatus.NOT_STARTED
MISSION_NAME_ONE = "BMission1"
MISSION_COMMENT_ONE = "La Mission 1"
MISSION_START_DATE_ONE = datetime.date(2020, 4, 20)
MISSION_END_DATE_ONE = datetime.date(2020, 4, 30)

MISSION_STATUS_TWO = MissionStatus.ON_GOING
MISSION_NAME_TWO = "AMission2"
MISSION_COMMENT_TWO = "La Mission 2"
MISSION_START_DATE_TWO = datetime.date(2020, 3, 10)
MISSION_END_DATE_TWO = datetime.date(2020, 4, 10)


def create_mission_one(agency_id, antenna_id, client_id) -> Mission:
    return Mission(
        status=MISSION_STATUS_ONE,
        name=MISSION_NAME_ONE,
        comment=MISSION_COMMENT_ONE,
        start_date=MISSION_START_DATE_ONE,
        end_date=MISSION_END_DATE_ONE,
        agency_id=agency_id,
        antenna_id=antenna_id,
        client_id=client_id,
    )


def create_mission_two(agency_id, antenna_id, client_id) -> Antenna:
    return Mission(
        status=MISSION_STATUS_TWO,
        name=MISSION_NAME_TWO,
        comment=MISSION_COMMENT_TWO,
        start_date=MISSION_START_DATE_TWO,
        end_date=MISSION_END_DATE_TWO,
        agency_id=agency_id,
        antenna_id=antenna_id,
        client_id=client_id,
    )


@fixture
def mission(
    antenna: Antenna, agency: Agency, client: Client, db: SQLAlchemy
) -> Mission:
    db.session.add(antenna)
    db.session.add(agency)
    db.session.add(client)
    db.session.commit()
    return create_mission_one(
        agency_id=agency.id, antenna_id=antenna.id, client_id=client.id
    )


@fixture
def mission_one(
    antenna: Antenna, agency: Agency, client: Client, db: SQLAlchemy
) -> Mission:
    m1: Mission = create_mission_one(
        agency_id=agency.id, antenna_id=antenna.id, client_id=client.id
    )
    db.session.add(m1)
    db.session.commit()
    return m1


@fixture
def mission_two(
    antenna: Antenna, agency: Agency, client: Client, db: SQLAlchemy
) -> Mission:
    m2: Mission = create_mission_two(
        agency_id=agency.id, antenna_id=antenna.id, client_id=client.id
    )
    db.session.add(m2)
    db.session.commit()
    return m2
