"""empty message

Revision ID: bd4b3a1e3625
Revises: 786cf16624b0
Create Date: 2022-03-03 09:46:58.467318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd4b3a1e3625'
down_revision = '786cf16624b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imports', sa.Column('label', sa.String(length=255), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('imports', 'label', schema='core')
    # ### end Alembic commands ###
