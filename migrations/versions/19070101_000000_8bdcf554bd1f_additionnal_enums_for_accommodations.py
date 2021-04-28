"""additionnal enums for accommodations

Revision ID: 8bdcf554bd1f
Revises: d7ed2adca9d3
Create Date: 2020-07-01 11:45:31.863242

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from requests import Session
from sqlalchemy import MetaData, Table

revision = "8bdcf554bd1f"
down_revision = "d7ed2adca9d3"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("enum",))
    enum_table = Table("enum", meta)

    additional_enums = {
        "ProjectAccommodationTypology": ["Studio",],
        "ProjectAccommodationAccess": ["Indépendant", "Par les parties communes"],
        "ProjectAccommodationRentTypeAfterRenovation": ["LL", "LI", "LCS", "LCTS"],
    }

    for i in range(1, 13):
        additional_enums["ProjectAccommodationTypology"].append(f"T{i}")

    rows = []
    current_date = datetime.utcnow()
    for kind, items in additional_enums.items():
        for i, name in enumerate(items):
            rows.append(
                {
                    "name": name,
                    "kind": kind,
                    "display_order": i + 1,
                    "private": True,
                    "disabled": False,
                    "created_at": current_date,
                    "updated_at": current_date,
                }
            )

    op.bulk_insert(
        enum_table, rows,
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "DELETE FROM core.enum WHERE kind = 'ProjectAccommodationTypology' OR kind = 'ProjectAccommodationAccess' OR kind = 'ProjectAccommodationRentTypeAfterRenovation';"
    )
