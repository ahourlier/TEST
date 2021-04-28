"""new enum kind perrenoud

Revision ID: 07a44648f4a3
Revises: ebe981d66522
Create Date: 2020-10-26 14:31:52.206524

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "07a44648f4a3"
down_revision = "ebe981d66522"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum_kind",))
    enum_perrenoud_kind_table = Table("perrenoud_enum_kind", meta)
    perrenoud_enums_key_labels = {
        11: None,
        39: "Type de Generateur",
        41: "Type d'émission",
        42: "Type de chauffage",
        43: "Type d'émetteur",
        44: "Equipement d'intermittence",
        46: "Type de Poêle",
        47: "Année Installation des émétteurs",
    }

    current_date = datetime.utcnow()
    rows = []
    for index, label in perrenoud_enums_key_labels.items():
        rows.append(
            {
                "index": index,
                "label": label,
                "created_at": current_date,
                "updated_at": current_date,
            }
        )

    op.bulk_insert(
        enum_perrenoud_kind_table, rows,
    )


def downgrade():
    pass
