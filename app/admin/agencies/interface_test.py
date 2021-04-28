from pytest import fixture

from .interface import AgencyInterface
from .model import Agency
from .model_test import AGENCY_NAME_ONE, AGENCY_ADDRESS_ONE, AGENCY_EMAIL_ONE


def get_agency_one_interface() -> AgencyInterface:
    return AgencyInterface(
        name=AGENCY_NAME_ONE,
        postal_address=AGENCY_ADDRESS_ONE,
        email_address=AGENCY_EMAIL_ONE,
    )


@fixture
def interface() -> AgencyInterface:
    return get_agency_one_interface()


def test_agency_interface_create(interface: AgencyInterface):
    assert interface


def test_agency_interface_ok(interface: AgencyInterface):
    user = Agency(**interface)
    assert user
