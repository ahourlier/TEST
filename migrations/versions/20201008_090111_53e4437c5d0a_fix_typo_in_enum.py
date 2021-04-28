"""fix typo in enum

Revision ID: 53e4437c5d0a
Revises: 69d61b51a9a0
Create Date: 2020-10-08 09:01:11.045036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = "53e4437c5d0a"
down_revision = "69d61b51a9a0"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum SET name='Remplacement des menuiseries peu performantes par des menuiseries double vitrage, avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.' WHERE name = 'Remplacement des menuiseries speu performantes par des menuiseries double vitrage, avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.';"
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum SET name='Remplacement des menuiseries speu performantes par des menuiseries double vitrage, avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.' WHERE name = 'Remplacement des menuiseries peu performantes par des menuiseries double vitrage, avec Uw <= 1,3W/m².K et Sw > 0,3 ou Uw <= 1,7W/m².K et Sw > 0,36.';"
    )
