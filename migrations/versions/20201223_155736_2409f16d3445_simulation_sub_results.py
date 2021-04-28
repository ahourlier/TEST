"""simulation sub results

Revision ID: 2409f16d3445
Revises: b0ae9f59c959
Create Date: 2020-12-23 15:57:36.593097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2409f16d3445"
down_revision = "b0ae9f59c959"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "simulation_sub_result",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("simulation_id", sa.Integer(), nullable=True),
        sa.Column("accommodation_id", sa.Integer(), nullable=True),
        sa.Column("work_price", sa.Float(), nullable=True),
        sa.Column("total_subvention", sa.Float(), nullable=True),
        sa.Column("remaining_cost", sa.Float(), nullable=True),
        sa.Column("subention_on_TTC", sa.Integer(), nullable=True),
        sa.Column("is_common_area", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["accommodation_id"],
            ["core.accommodation.id"],
            name=op.f("fk_simulation_sub_result_accommodation_id_accommodation"),
        ),
        sa.ForeignKeyConstraint(
            ["simulation_id"],
            ["core.simulation.id"],
            name=op.f("fk_simulation_sub_result_simulation_id_simulation"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_simulation_sub_result")),
        schema="core",
    )
    op.drop_column("funder_accommodations", "work_price", schema="core")
    op.drop_column("funder_accommodations", "remaining_cost", schema="core")
    op.drop_column("funder_accommodations", "subvention_on_TTC", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "funder_accommodations",
        sa.Column(
            "subvention_on_TTC", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "funder_accommodations",
        sa.Column(
            "remaining_cost",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        schema="core",
    )
    op.add_column(
        "funder_accommodations",
        sa.Column(
            "work_price",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        schema="core",
    )
    op.drop_table("simulation_sub_result", schema="core")
    # ### end Alembic commands ###
