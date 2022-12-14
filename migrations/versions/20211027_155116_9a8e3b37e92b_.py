"""empty message

Revision ID: 9a8e3b37e92b
Revises: fe580df46bd9
Create Date: 2021-10-27 15:51:16.155142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9a8e3b37e92b'
down_revision = 'fe580df46bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'referent',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('function', sa.String(length=255), nullable=True),
        sa.Column('mission_id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['mission_id'], ['core.mission.id'],
                                name=op.f('fk_referent_mission_id_mission')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_referent')),
        schema='core'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referent', schema='core')
    # ### end Alembic commands ###
