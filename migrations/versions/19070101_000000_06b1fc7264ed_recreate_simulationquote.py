"""recreate simulationquote

Revision ID: 06b1fc7264ed
Revises: 23acaac06ed0
Create Date: 2020-06-09 15:31:21.714202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06b1fc7264ed"
down_revision = "23acaac06ed0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "simulation_quote",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("base_quote_id", sa.Integer(), nullable=True),
        sa.Column("duplicate_quote_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["base_quote_id"],
            ["core.quote.id"],
            name=op.f("fk_simulation_quote_base_quote_id_quote"),
        ),
        sa.ForeignKeyConstraint(
            ["duplicate_quote_id"],
            ["core.quote.id"],
            name=op.f("fk_simulation_quote_duplicate_quote_id_quote"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_simulation_quote")),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("simulation_quote", schema="core")
    # ### end Alembic commands ###