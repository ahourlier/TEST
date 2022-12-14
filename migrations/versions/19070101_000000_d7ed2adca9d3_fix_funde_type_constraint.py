"""Fix funde type constraint

Revision ID: d7ed2adca9d3
Revises: 014673597f25
Create Date: 2020-06-30 18:14:55.254898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d7ed2adca9d3"
down_revision = "014673597f25"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "funder",
        sa.Column("requester_type", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "funding_scenario",
        sa.Column("upper_price_surface_limit", sa.Integer(), nullable=True),
        schema="core",
    )
    op.add_column(
        "funding_scenario",
        sa.Column("upper_surface_limit", sa.Integer(), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("funding_scenario", "upper_surface_limit", schema="core")
    op.drop_column("funding_scenario", "upper_price_surface_limit", schema="core")
    op.drop_column("funder", "requester_type", schema="core")
    # ### end Alembic commands ###
