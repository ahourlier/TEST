"""empty message

Revision ID: 2c1bac5afa04
Revises: cc1c0c7afd84
Create Date: 2022-04-20 16:07:44.484110

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = '2c1bac5afa04'
down_revision = 'cc1c0c7afd84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")

    kind = "StepStatus"
    values = ['Non débutée', 'En cours', 'Terminée', 'Non concernée']
    for value in values:
        session.execute(
            "INSERT INTO core.enum (created_at, updated_at, kind, name, display_order, disabled, private) VALUES "
            f"('{now}', '{now}', '{kind}', '{value}', NULL, false, false)"
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)

    kind = "StepStatus"
    session.execute(
        f"DELETE FROM core.enum WHERE kind = '{kind}';"
    )
    # ### end Alembic commands ###