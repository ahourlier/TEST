"""empty message

Revision ID: b16e2c5183aa
Revises: bd4b3a1e3625
Create Date: 2022-03-03 13:53:02.589845

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b16e2c5183aa'
down_revision = 'b9f54bb64372'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('simulation_accommodation', sa.Column('scenario_id', sa.Integer(), nullable=True), schema='core')
    op.create_foreign_key(op.f('fk_simulation_accommodation_scenario_id_scenario'), 'simulation_accommodation', 'scenario', ['scenario_id'], ['id'], source_schema='core', referent_schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_simulation_accommodation_scenario_id_scenario'), 'simulation_accommodation', schema='core', type_='foreignkey')
    op.drop_column('simulation_accommodation', 'scenario_id', schema='core')
    # ### end Alembic commands ###
