from pytest import fixture

from .model import Antenna
from .interface import AntennaInterface
from .model_test import (
    ANTENNA_NAME_ONE,
    ANTENNA_ADDRESS_ONE,
    ANTENNA_EMAIL_ONE,
)


def get_antenna_one_interface() -> AntennaInterface:
    return AntennaInterface(
        name=ANTENNA_NAME_ONE,
        postal_address=ANTENNA_ADDRESS_ONE,
        email_address=ANTENNA_EMAIL_ONE,
        agency_id=1,
    )


@fixture
def interface() -> AntennaInterface:
    return get_antenna_one_interface()


def test_antenna_interface_create(interface: AntennaInterface):
    assert interface


def test_antenna_interface_ok(interface: AntennaInterface):
    antenna = Antenna(**interface)
    assert antenna
