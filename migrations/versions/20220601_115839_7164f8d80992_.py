"""empty message

Revision ID: 7164f8d80992
Revises: f90e6bb49417
Create Date: 2022-06-01 11:58:39.797101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7164f8d80992'
down_revision = 'f90e6bb49417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('copro', sa.Column('nb_aerial_parking_spaces', sa.Integer(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('nb_underground_parking_spaces', sa.Integer(), nullable=True), schema='core')
    op.drop_column('copro', 'aerial_parking', schema='core')
    op.drop_column('copro', 'underground_parking', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('copro', sa.Column('underground_parking', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('copro', sa.Column('aerial_parking', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.drop_column('copro', 'nb_underground_parking_spaces', schema='core')
    op.drop_column('copro', 'nb_aerial_parking_spaces', schema='core')
    # ### end Alembic commands ###