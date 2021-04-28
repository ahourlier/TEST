"""add additional enums

Revision ID: 1e3b31caadbe
Revises: ce8f21ffbe03
Create Date: 2020-05-20 15:21:02.869706

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

revision = "1e3b31caadbe"
down_revision = "ce8f21ffbe03"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("enum",))
    enum_table = Table("enum", meta)

    additional_enums = {
        "ProjectRequesterResourceCategory": [
            "Modeste",
            "Très modeste",
            "Autre éligible",
            "Hors Plafond",
        ],
        "ProjectRequesterProfessionType": [
            "Salarié entreprise cotisante PEEC",
            "Retraité entreprise cotisante PEEC",
            "Salarié autre",
            "Retraité autre",
            "Sans emploi",
        ],
    }

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
        "DELETE FROM core.enum WHERE kind = 'ProjectRequesterResourceCategory' OR kind = 'ProjectRequesterProfessionType';"
    )
