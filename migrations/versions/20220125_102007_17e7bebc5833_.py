"""empty message

Revision ID: 17e7bebc5833
Revises: 4ec050767555
Create Date: 2022-01-25 10:20:07.247066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17e7bebc5833'
down_revision = '4ec050767555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('combined_structure', 'cctv', schema='core')
    op.drop_column('combined_structure', 'underground_parking', schema='core')
    op.drop_column('combined_structure', 'other_equipments_details', schema='core')
    op.drop_column('combined_structure', 'other_equipments', schema='core')
    op.drop_column('combined_structure', 'aerial_parking', schema='core')
    op.drop_column('combined_structure', 'heater', schema='core')
    op.drop_column('combined_structure', 'green_spaces', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('combined_structure', sa.Column('green_spaces', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('heater', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('aerial_parking', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('other_equipments', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('other_equipments_details', sa.TEXT(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('underground_parking', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('combined_structure', sa.Column('cctv', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    # ### end Alembic commands ###
