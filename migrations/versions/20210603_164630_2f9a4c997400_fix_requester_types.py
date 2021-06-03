"""empty message

Revision ID: 2f9a4c997400
Revises: aded195b5e2a
Create Date: 2021-06-03 16:46:30.610640

"""
from alembic import op
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = '2f9a4c997400'
down_revision = 'aded195b5e2a'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum "
        "SET name = 'TENANT' "
        "WHERE kind = 'ProjectRequesterType' AND display_order = 3"
    )
    session.execute(
        "UPDATE core.enum "
        "SET name = 'SDC' "
        "WHERE kind = 'ProjectRequesterType' AND display_order = 4"
    )
    session.execute(
        "UPDATE core.requester "
        "SET type = 'TENANT' "
        "WHERE type = 'Locataire'"
    )
    session.execute(
        "UPDATE core.requester "
        "SET type = 'SDC' "
        "WHERE type = 'SDC (Syndicat des Copropriétaires)'"
    )
    session.execute(
        "UPDATE core.funder "
        "SET requester_type = 'TENANT' "
        "WHERE requester_type = 'Locataire'"
    )
    session.execute(
        "UPDATE core.funder "
        "SET requester_type = 'SDC' "
        "WHERE requester_type = 'SDC (Syndicat des Copropriétaires)'"
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.enum "
        "SET name = 'Locataire' "
        "WHERE kind = 'ProjectRequesterType' AND display_order = 3"
    )
    session.execute(
        "UPDATE core.enum "
        "SET name = 'SDC (Syndicat des Copropriétaires)' "
        "WHERE kind = 'ProjectRequesterType' AND display_order = 4"
    )
    session.execute(
        "UPDATE core.requester "
        "SET type = 'Locataire' "
        "WHERE type = 'TENANT'"
    )
    session.execute(
        "UPDATE core.requester "
        "SET type = 'SDC (Syndicat des Copropriétaires)' "
        "WHERE type = 'SDC'"
    )
    session.execute(
        "UPDATE core.funder "
        "SET requester_type = 'Locataire' "
        "WHERE requester_type = 'TENANT'"
    )
    session.execute(
        "UPDATE core.funder "
        "SET requester_type = 'SDC (Syndicat des Copropriétaires)' "
        "WHERE requester_type = 'SDC'"
    )
