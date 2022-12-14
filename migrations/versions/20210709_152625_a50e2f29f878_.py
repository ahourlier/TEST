"""empty message

Revision ID: a50e2f29f878
Revises: 376cb90e6ca9
Create Date: 2022-02-08 12:37:12.838725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a50e2f29f878'
down_revision = '376cb90e6ca9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('required_action', sa.Boolean(), server_default='False', nullable=False), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'required_action', schema='core')
    # ### end Alembic commands ###
