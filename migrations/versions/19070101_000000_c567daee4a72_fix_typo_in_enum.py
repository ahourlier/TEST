"""fix typo in enum

Revision ID: c567daee4a72
Revises: dd76ae047670
Create Date: 2020-05-18 16:58:47.779751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = "c567daee4a72"
down_revision = "dd76ae047670"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum SET name='SDC (Syndicat des Copropriétaires)' WHERE name = 'SDC (Syndicat des Copropriétaires';"
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum SET name='SDC (Syndicat des Copropriétaires' WHERE name = 'SDC (Syndicat des Copropriétaires)';"
    )
