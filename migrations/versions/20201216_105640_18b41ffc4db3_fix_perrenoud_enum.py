"""fix perrenoud_enums

Revision ID: 18b41ffc4db3
Revises: 238e6c3038cc
Create Date: 2020-12-16 10:56:40.962972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = "18b41ffc4db3"
down_revision = "238e6c3038cc"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Garage' WHERE label = 'Maison individuelle - Garage';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Véranda' WHERE label = 'Maison individuelle - Véranda';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Cellier' WHERE label = 'Maison individuelle - Cellier';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Comble fortement ventilé' WHERE label = 'Maison individuelle - Comble fortement ventilé';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Comble faiblement ventilé' WHERE label = 'Maison individuelle - Comble faiblement ventilé';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Sous-sol' WHERE label = 'Maison individuelle - Sous-sol';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Hors volume habitable' WHERE label = 'Hors volume habitabl';"
    )


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Maison individuelle - Garage' WHERE label = 'Garage';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Maison individuelle - Véranda' WHERE label = 'Véranda';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Maison individuelle - Cellier' WHERE label = 'Cellier';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Maison individuelle - Comble fortement ventilé' WHERE label = 'Comble fortement ventilé';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Comble faiblement ventilé' WHERE label = 'Comble faiblement ventilé';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Maison individuelle - Sous-sol' WHERE label = 'Maison individuelle - Sous-sol';"
    )
    session.execute(
        "UPDATE core.perrenoud_enum SET label='Hors volume habitabl' WHERE label = 'Hors volume habitable';"
    )
