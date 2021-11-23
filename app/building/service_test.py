import pytest
from flask_sqlalchemy import SQLAlchemy

from app.building.exceptions import WrongConstructionTimeException
from app.building.interface import BuildingInterface
from app.building.service import BuildingService
# from app.building import Building
# from app.copro.copros.model import Copro

MOCK_COPRO = {
    "address_1": {
        "full_address": "7 Rue Montaubert, Saint-Mard, France",
        "number": "7",
        "street": "Rue Montaubert",
        "city": "Saint-Mard",
        "postal_code": "77230",
        "additional_info": None
    },
    "copro_type": "Copropriété",
}

MOCK_BUILDING = BuildingInterface(**{
    "name": "test building",
    "construction_time": "< 1850",
    "address": {
        "full_address": "7 Rue Montaubert, Saint-Mard, France",
        "number": "7",
        "street": "Rue Montaubert",
        "city": "Saint-Mard",
        "postal_code": "77230",
        "additional_info": None
    },
    "copro_id": 0
})

COPRO_TYPE = {
    "kind": "CoproType",
    "name": "Copropriété"
}

CONSTRUCTION_TIME = {
    "kind": "CoproType",
    "name": "Copropriété"
}


# def create_copro(db_instance) -> Copro:
#     created_copro = Copro(**MOCK_COPRO)
#     db_instance.session.add(created_copro)
#     db_instance.session.commit()
#     return created_copro


def test_create(db: SQLAlchemy):
    # created_copro = create_copro(db)
    building_payload = MOCK_BUILDING
    building_payload["copro_id"] = 1
    # with pytest.raises(WrongConstructionTimeException):
    BuildingService.create(building_payload)
