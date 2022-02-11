"""empty message

Revision ID: b6ea8de7b31d
Revises: 4e8156e991ce
Create Date: 2021-10-26 16:08:27.001347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from app.common.app_name import App

revision = 'b6ea8de7b31d'
down_revision = '4e8156e991ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mission', sa.Column('ca_asl_screen', sa.Boolean(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('ca_building_screen', sa.Boolean(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('ca_copro_screen', sa.Boolean(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('ca_lot_screen', sa.Boolean(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('ca_mission_screen', sa.Boolean(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('mission_end_date', sa.Date(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('mission_start_date', sa.Date(), nullable=True), schema='core')
    op.add_column('mission', sa.Column('mission_type', sa.String(length=255), nullable=True), schema='core')
    op.execute(f"UPDATE core.mission SET mission_type = '{App.INDIVIDUAL}'")
    op.execute("ALTER TABLE core.mission ALTER COLUMN mission_type SET NOT NULL")
    # op.alter_column('mission', 'mission_type', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mission', 'mission_type', schema='core')
    op.drop_column('mission', 'mission_start_date', schema='core')
    op.drop_column('mission', 'mission_end_date', schema='core')
    op.drop_column('mission', 'ca_mission_screen', schema='core')
    op.drop_column('mission', 'ca_lot_screen', schema='core')
    op.drop_column('mission', 'ca_copro_screen', schema='core')
    op.drop_column('mission', 'ca_building_screen', schema='core')
    op.drop_column('mission', 'ca_asl_screen', schema='core')
    # ### end Alembic commands ###
