from flask_sqlalchemy import SQLAlchemy

from app.common.address.model import Address
from app.common.phone_number.model import PhoneNumber
from app.copro.moe import Moe
from app.copro.moe.service import MoeService
from app.test.fixtures import app, db
from app.copro.moe.interface import MoeInterface

mock_moe = MoeInterface(**{
    "name": "Test MOE",
    "address": {
        "full_address": "9 rue de la chose, 69120 Vaulx-en-Velin, France",
        "postal_code": "69120",
        "street": "rue de la chose",
        "number": "9",
        "additional_info": "",
        "city": "Vaulx-en-Velin"
    },
    "phone_number": {
        "international": "test",
        "country_code": "FRA",
        "national": "test"
    }
})


def test_create(db: SQLAlchemy):
    list_moe = Moe.query.all()
    assert len(list_moe) == 0
    moe_id = MoeService.create(mock_moe)
    assert moe_id is not None
    list_moe = Moe.query.all()
    assert len(list_moe) == 1


def test_update(db: SQLAlchemy):
    new_moe_interface = mock_moe
    address = new_moe_interface.get("address")
    phone = new_moe_interface.get("phone_number")
    del new_moe_interface["address"]
    del new_moe_interface["phone_number"]
    new_address = Address(**address)
    db.session.add(new_address)
    db.session.commit()
    new_moe = Moe(**dict(mock_moe))
    new_moe.address_id = new_address.id
    db.session.add(new_moe)
    db.session.commit()
    phone["resource_type"] = "moe"
    phone["resource_id"] = new_moe.id
    new_phone = PhoneNumber(**phone)
    db.session.add(new_phone)
    db.session.commit()
    assert new_moe.id is not None
    assert new_moe.address is not None
    assert new_moe.phone_number is not None
    new_name = "Test updated from test"
    new_full_address = "une nouvelle address updated"
    new_international = "updated test"
    MoeService.update(new_moe, MoeInterface(**{
        "name": new_name,
        "address": {
            "full_address": new_full_address
        },
        "phone_number": {
            "id": new_phone.id,
            "international": new_international
        }
    }))
    assert new_moe.address.full_address == new_full_address
    assert new_moe.name == new_name
    assert new_moe.phone_number.international == new_international
