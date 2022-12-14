"""empty message

Revision ID: fc7c92ced175
Revises: d8463c0cb6bd
Create Date: 2021-11-09 14:23:45.634570

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fc7c92ced175'
down_revision = 'd8463c0cb6bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('elect',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('mission_details_id', sa.Integer(), nullable=False),
                    sa.Column('last_name', sa.String(length=255), nullable=True),
                    sa.Column('first_name', sa.String(length=255), nullable=True),
                    sa.Column('function', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['mission_details_id'], ['core.mission_detail.id'],
                                            name=op.f('fk_elect_mission_details_id_mission_detail')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_elect')),
                    schema='core'
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('elect', schema='core')
    # ### end Alembic commands ###
