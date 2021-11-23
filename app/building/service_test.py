from flask_sqlalchemy import SQLAlchemy

from app.copro.copros.model import Copro

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

MOCK_BUILDING = {
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
    "copro_id": None
}

COPRO_TYPE = {
    "kind": "CoproType",
    "name": "Copropriété"
}

CONSTRUCTION_TIME = {
    "kind": "CoproType",
    "name": "Copropriété"
}

def create_copro(db):
    created_copro = Copro(**MOCK_COPRO)
    db.session.add(created_copro)
    db.session.commit()
    return created_copro


def test_create(db: SQLAlchemy):
    created_copro = create_copro(db)
