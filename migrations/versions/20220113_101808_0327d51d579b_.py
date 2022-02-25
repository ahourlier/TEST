"""empty message

Revision ID: 0327d51d579b
Revises: 07774bccc88f
Create Date: 2022-01-13 10:18:08.006581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0327d51d579b'
down_revision = '07774bccc88f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('date', sa.Date(), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'date', schema='core')
    # ### end Alembic commands ###