"""update manager role

Revision ID: 1be295f0450a
Revises: 2ccc8e5a2201
Create Date: 2020-05-13 16:03:59.968359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = "1be295f0450a"
down_revision = "2ccc8e5a2201"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.team SET user_position='mission_manager' WHERE user_position = 'manager';"
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.team SET user_position='manager' WHERE user_position = 'mission_manager';"
    )
