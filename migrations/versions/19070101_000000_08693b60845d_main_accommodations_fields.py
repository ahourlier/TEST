"""main_accommodations_fields

Revision ID: 08693b60845d
Revises: 4123a02a4e1d
Create Date: 2020-06-30 15:24:41.400054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "08693b60845d"
down_revision = "4123a02a4e1d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accommodation",
        sa.Column("address_complement", sa.String(length=800), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("adults_tenants_number", sa.Integer(), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("current_rent", sa.Float(), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("degradation_coefficient", sa.Float(), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("minors_tenants_number", sa.Integer(), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("name", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("out_of_project", sa.Boolean(create_constraint=False), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("rent_after_renovation", sa.Float(), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("tenant_commentary", sa.String(length=800), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("tenant_email", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("tenant_first_name", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("tenant_last_name", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("tenant_title", sa.String(length=10), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("typology", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "accommodation",
        sa.Column("unsanitary_coefficient", sa.Float(), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("accommodation", "unsanitary_coefficient", schema="core")
    op.drop_column("accommodation", "typology", schema="core")
    op.drop_column("accommodation", "tenant_title", schema="core")
    op.drop_column("accommodation", "tenant_last_name", schema="core")
    op.drop_column("accommodation", "tenant_first_name", schema="core")
    op.drop_column("accommodation", "tenant_email", schema="core")
    op.drop_column("accommodation", "tenant_commentary", schema="core")
    op.drop_column("accommodation", "rent_after_renovation", schema="core")
    op.drop_column("accommodation", "out_of_project", schema="core")
    op.drop_column("accommodation", "name", schema="core")
    op.drop_column("accommodation", "minors_tenants_number", schema="core")
    op.drop_column("accommodation", "degradation_coefficient", schema="core")
    op.drop_column("accommodation", "current_rent", schema="core")
    op.drop_column("accommodation", "adults_tenants_number", schema="core")
    op.drop_column("accommodation", "address_complement", schema="core")
    # ### end Alembic commands ###
