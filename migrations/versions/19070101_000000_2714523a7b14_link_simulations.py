"""link simulations

Revision ID: 2714523a7b14
Revises: 06b1fc7264ed
Create Date: 2020-06-09 15:45:30.608854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2714523a7b14"
down_revision = "06b1fc7264ed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "simulation_funder",
        sa.Column("simulation_id", sa.Integer(), nullable=True),
        schema="core",
    )
    op.create_foreign_key(
        op.f("fk_simulation_funder_simulation_id_simulation"),
        "simulation_funder",
        "simulation",
        ["simulation_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    op.add_column(
        "simulation_quote",
        sa.Column("simulation_id", sa.Integer(), nullable=True),
        schema="core",
    )
    op.create_foreign_key(
        op.f("fk_simulation_quote_simulation_id_simulation"),
        "simulation_quote",
        "simulation",
        ["simulation_id"],
        ["id"],
        source_schema="core",
        referent_schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_simulation_quote_simulation_id_simulation"),
        "simulation_quote",
        schema="core",
        type_="foreignkey",
    )
    op.drop_column("simulation_quote", "simulation_id", schema="core")
    op.drop_constraint(
        op.f("fk_simulation_funder_simulation_id_simulation"),
        "simulation_funder",
        schema="core",
        type_="foreignkey",
    )
    op.drop_column("simulation_funder", "simulation_id", schema="core")
    # ### end Alembic commands ###
