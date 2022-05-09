"""empty message

Revision ID: cc1c0c7afd84
Revises: d24c1f1d999b
Create Date: 2022-04-20 16:07:44.484110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc1c0c7afd84'
down_revision = 'd24c1f1d999b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historic', sa.Column('version_id', sa.String(), nullable=False), schema='core')
    op.drop_column('historic', 'thematique_id', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historic', sa.Column('thematique_id', sa.VARCHAR(), autoincrement=False, nullable=False), schema='core')
    op.drop_column('historic', 'version_id', schema='core')
    # ### end Alembic commands ###