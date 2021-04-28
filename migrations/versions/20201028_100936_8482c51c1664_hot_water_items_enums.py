""" hot water enums

Revision ID: 8482c51c1664
Revises: e8ebbf872951
Create Date: 2020-10-28 10:09:36.065046

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "8482c51c1664"
down_revision = "e8ebbf872951"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum",))
    perrenoud_enums = Table("perrenoud_enum", meta)
    # 48, 52, 58, 50, 51,  60
    new_perrenoud_enums = {
        48: [
            {"value": 101, "label": "Electrique"},
            {
                "value": 102,
                "label": "Chauffe - eau thermo sur air ext.ou ambiant ou PAC double service",
            },
            {"value": 201, "label": "Générateur mixte(chauffage + ecs)"},
            {"value": 203, "label": "Accumulateur gaz"},
            {"value": 204, "label": "chauffe bain gaz instantané"},
        ],
        52: [{"value": 0, "label": "Vertical"}, {"value": 1, "label": "Horizontal"}],
        58: [
            {"value": 0, "label": "Avant 1990"},
            {"value": 1, "label": "De 1990 à 2000"},
            {"value": 2, "label": "Après 2000"},
        ],
        50: [
            {"value": 0, "label": "En volume habitable"},
            {"value": 1, "label": "Hors volume habitabl"},
        ],
        51: [
            {"value": 0, "label": "Instantanée"},
            {"value": 1, "label": "Accumulation"},
        ],
        60: [
            {"value": 0, "label": "Production ECS solaire"},
            {"value": 1, "label": "Système combiné chauffage / ECS solaire"},
        ],
    }

    current_date = datetime.utcnow()
    rows = []
    for index, items in new_perrenoud_enums.items():
        for item in items:
            rows.append(
                {
                    "index": index,
                    "value": item.get("value"),
                    "label": item.get("label"),
                    "created_at": current_date,
                    "updated_at": current_date,
                }
            )


def downgrade():
    pass
