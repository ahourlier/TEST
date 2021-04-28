"""match_scenario

Revision ID: 26d0a23f8160
Revises: fae89d89e094
Create Date: 2020-06-18 13:21:40.672332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26d0a23f8160"
down_revision = "fae89d89e094"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "simulation_funder",
        sa.Column("match_scenario_id", sa.Integer(), nullable=True),
        schema="core",
    )
    op.create_foreign_key(
        op.f("fk_simulation_funder_match_scenario_id_funding_scenario"),
        "simulation_funder",
        "funding_scenario",
        ["match_scenario_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_simulation_funder_match_scenario_id_funding_scenario"),
        "simulation_funder",
        schema="core",
        type_="foreignkey",
    )
    op.drop_column("simulation_funder", "match_scenario_id", schema="core")
    # ### end Alembic commands ###
