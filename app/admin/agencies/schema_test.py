from pytest import fixture

from .model import Agency
from .model_test import AGENCY_NAME_ONE, AGENCY_ADDRESS_ONE, AGENCY_EMAIL_ONE
from .schema import AgencySchema


@fixture
def schema() -> AgencySchema:
    return AgencySchema()


def test_agency_schema_create(schema: AgencySchema):
    assert schema


def test_agency_schema_ok(schema: AgencySchema):
    params = schema.load(
        {
            "name": AGENCY_NAME_ONE,
            "postal_address": AGENCY_ADDRESS_ONE,
            "email_address": AGENCY_EMAIL_ONE,
        }
    )

    agency = Agency(**params)

    assert agency.name == AGENCY_NAME_ONE
    assert agency.postal_address == AGENCY_ADDRESS_ONE
    assert agency.email_address == AGENCY_EMAIL_ONE
