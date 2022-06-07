"""empty message

Revision ID: d24c1f1d999b
Revises: 9ad87acb91aa
Create Date: 2022-04-19 13:54:23.713861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd24c1f1d999b'
down_revision = '9ad87acb91aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('historic',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('thematique_id', sa.String(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.Column('status_changed', sa.Boolean(), nullable=False),
    sa.Column('old_status', sa.String(), nullable=True),
    sa.Column('new_status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['updated_by_id'], ['core.user.id'], name=op.f('fk_historic_updated_by_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_historic')),
    schema='core'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('historic', schema='core')
    # ### end Alembic commands ###
