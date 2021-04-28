"""url perrenoud

Revision ID: c3c3cd9b01c7
Revises: 5ac850ea2d37
Create Date: 2020-12-07 14:50:45.216745

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "c3c3cd9b01c7"
down_revision = "5ac850ea2d37"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("app_config",))
    app_config_table = Table("app_config", meta)
    new_config_key = {
        "perrenoud_url": "http://wsu.logicielsperrenoud.fr/ws3cl.ashx",
    }

    current_date = datetime.utcnow()
    rows = []
    for key, value in new_config_key.items():
        rows.append(
            {
                "key": key,
                "value": value,
                "created_at": current_date,
                "updated_at": current_date,
            }
        )

    op.bulk_insert(
        app_config_table, rows,
    )


def downgrade():
    pass
