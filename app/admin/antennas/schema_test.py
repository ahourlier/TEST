from pytest import fixture

from app.admin.antennas import Antenna
from app.admin.antennas.model_test import (
    ANTENNA_NAME_ONE,
    ANTENNA_ADDRESS_ONE,
    ANTENNA_EMAIL_ONE,
)
from app.admin.antennas.schema import AntennaSchema


@fixture
def schema() -> AntennaSchema:
    return AntennaSchema()


def test_antenna_schema_create(schema: AntennaSchema):
    assert schema


def test_antenna_schema_ok(schema: AntennaSchema):
    params = schema.load(
        {
            "name": ANTENNA_NAME_ONE,
            "postal_address": ANTENNA_ADDRESS_ONE,
            "email_address": ANTENNA_EMAIL_ONE,
            "agency_id": 1,
        }
    )

    antenna = Antenna(**params)

    assert antenna.name == ANTENNA_NAME_ONE
    assert antenna.postal_address == ANTENNA_ADDRESS_ONE
    assert antenna.email_address == ANTENNA_EMAIL_ONE
    assert antenna.agency_id == 1
