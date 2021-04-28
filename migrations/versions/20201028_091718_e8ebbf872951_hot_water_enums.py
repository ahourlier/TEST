"""hot water enums

Revision ID: e8ebbf872951
Revises: 66d734c87f4f
Create Date: 2020-10-28 09:17:18.322173

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

# 48, 52, 58, 50, 51,  60

# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "e8ebbf872951"
down_revision = "66d734c87f4f"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum_kind",))
    enum_perrenoud_kind_table = Table("perrenoud_enum_kind", meta)
    perrenoud_enums_key_labels = {
        48: "Type d'ECS",
        52: "Type de chauffe-eau électrique",
        58: "Année accumulateur classique",
        50: "Position production ECS",
        51: "Position Instantannée ou Accumulée",
        60: "Type d'installation solaire",
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
