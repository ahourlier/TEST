"""empty message

Revision ID: 3e8709f3af6d
Revises: 1a8a8d1d46e7
Create Date: 2022-01-12 14:15:09.265290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = '3e8709f3af6d'
down_revision = '1a8a8d1d46e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mission_detail', 'market_number',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=True,
               schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute('ALTER TABLE core.mission_detail ALTER COLUMN market_number TYPE integer USING (market_number::integer)')
    # ### end Alembic commands ###
