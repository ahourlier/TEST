"""empty message

Revision ID: 46116ada951e
Revises: 916eac5ed2e5
Create Date: 2022-06-09 10:47:24.905307

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = '46116ada951e'
down_revision = '916eac5ed2e5'
branch_labels = None
depends_on = None

enums = {
    "HeightClassification": [
       "Sans classification",
       "IMH",
       "IGH",
       "NR",
       "Autre",
    ]
}

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('building', sa.Column('imh', sa.Boolean(), nullable=True), schema='core')
    op.add_column('building', sa.Column('height_classification', sa.String(length=255), nullable=True), schema='core')
    
    bind = op.get_bind()
    session = Session(bind=bind)
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Add not existing enums
    for (kind, values) in enums.items():
        for value in values:
            session.execute(
                "INSERT INTO core.enum (created_at, updated_at, kind, name, display_order, disabled, private) VALUES "
                f"('{now}', '{now}', '{kind}', '{value}', NULL, false, false);"
            )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('building', 'height_classification', schema='core')
    op.drop_column('building', 'imh', schema='core')
    
    bind = op.get_bind()
    session = Session(bind=bind)
    # Remove not existing enums
    for (kind, values) in enums.items():
        for value in values:
            session.execute(
                f"DELETE FROM core.enum WHERE kind = '{kind}' AND name = '{value}';"
            )
    # ### end Alembic commands ###