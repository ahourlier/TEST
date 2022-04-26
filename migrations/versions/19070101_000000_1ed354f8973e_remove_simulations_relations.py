"""remove simulations relations

Revision ID: 1ed354f8973e
Revises: fdeeec0ae386
Create Date: 2020-06-09 13:55:57.424187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1ed354f8973e"
down_revision = "fdeeec0ae386"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("funder_simulation", schema="core")
    op.drop_table("quote_simulation", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "quote_simulation",
        sa.Column("quote_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("simulation_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["quote_id"], ["core.quote.id"], name="fk_quote_simulation_quote_id_quote"
        ),
        sa.ForeignKeyConstraint(
            ["simulation_id"],
            ["core.simulation.id"],
            name="fk_quote_simulation_simulation_id_simulation",
        ),
        schema="core",
    )
    op.create_table(
        "funder_simulation",
        sa.Column("funder_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("simulation_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["funder_id"],
            ["core.funder.id"],
            name="fk_funder_simulation_funder_id_funder",
        ),
        sa.ForeignKeyConstraint(
            ["simulation_id"],
            ["core.simulation.id"],
            name="fk_funder_simulation_simulation_id_simulation",
        ),
        schema="core",
    )
    # ### end Alembic commands ###