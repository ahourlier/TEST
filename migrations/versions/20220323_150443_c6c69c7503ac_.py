"""empty message

Revision ID: c6c69c7503ac
Revises: d136e7d303e1
Create Date: 2022-03-23 15:04:43.524085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6c69c7503ac'
down_revision = 'd136e7d303e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lot', sa.Column('client_number', sa.String(length=255), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lot', 'client_number', schema='core')
    # ### end Alembic commands ###
