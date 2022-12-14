"""funder_simulation

Revision ID: fdeeec0ae386
Revises: 58c83a42ab07
Create Date: 2020-05-27 14:38:11.601007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fdeeec0ae386"
down_revision = "58c83a42ab07"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "funder_simulation",
        sa.Column("funder_id", sa.Integer(), nullable=True),
        sa.Column("simulation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["funder_id"],
            ["core.funder.id"],
            name=op.f("fk_funder_simulation_funder_id_funder"),
        ),
        sa.ForeignKeyConstraint(
            ["simulation_id"],
            ["core.simulation.id"],
            name=op.f("fk_funder_simulation_simulation_id_simulation"),
        ),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("funder_simulation", schema="core")
    # ### end Alembic commands ###
