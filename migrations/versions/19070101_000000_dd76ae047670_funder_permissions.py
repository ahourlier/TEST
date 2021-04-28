"""funder permissions

Revision ID: dd76ae047670
Revises: f07e6ca8c314
Create Date: 2020-05-18 16:46:00.680222

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from app.auth.users.model import UserRole

revision = "dd76ae047670"
down_revision = "f07e6ca8c314"
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind(), schema="core")

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=("permission",))

    # define table representation
    permission_table = Table("permission", meta)

    # insert records
    op.bulk_insert(
        permission_table,
        [
            {
                "entity": "funder",
                "action": "create",
                "role_id": UserRole.ADMIN,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder",
                "action": "delete",
                "role_id": UserRole.ADMIN,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder",
                "action": "read",
                "role_id": UserRole.MANAGER,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder",
                "action": "update",
                "role_id": UserRole.ADMIN,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder_mission",
                "action": "create",
                "role_id": UserRole.MANAGER,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder_mission",
                "action": "delete",
                "role_id": UserRole.MANAGER,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder_mission",
                "action": "read",
                "role_id": UserRole.MANAGER,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "entity": "funder_mission",
                "action": "update",
                "role_id": UserRole.MANAGER,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        ],
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "DELETE FROM core.permission WHERE entity = 'funder' OR entity = 'funder_mission';"
    )
