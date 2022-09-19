"""fix perrenoud tables types

Revision ID: de2c83fbc09b
Revises: 3455482e7a18
Create Date: 2020-10-29 17:42:20.715617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "de2c83fbc09b"
down_revision = "3455482e7a18"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ceiling",
        "insulated_heated_non_heated_wall",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Boolean(),
        existing_nullable=True,
        schema="core",
        postgresql_using="insulated_heated_non_heated_wall::boolean",
    )
    op.alter_column(
        "ceiling",
        "insulated_non_heated_exterior_wall",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Boolean(),
        existing_nullable=True,
        schema="core",
        postgresql_using="insulated_non_heated_exterior_wall::boolean",
    )
    op.alter_column(
        "ceiling",
        "insulated_wall",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Boolean(),
        existing_nullable=True,
        schema="core",
        postgresql_using="insulated_wall::boolean",
    )
    op.alter_column(
        "ceiling",
        "known_U_value",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Boolean(),
        existing_nullable=True,
        schema="core",
        postgresql_using='"known_U_value"::boolean',
    )
    op.drop_column("heating", "heated_area", schema="core")
    op.add_column(
        "hot_water",
        sa.Column("solar_device_type", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "wall", sa.Column("known_value", sa.Float(), nullable=True), schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("wall", "known_value", schema="core")
    op.drop_column("hot_water", "solar_device_type", schema="core")
    op.add_column(
        "heating",
        sa.Column(
            "heated_area",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        schema="core",
    )
    op.alter_column(
        "ceiling",
        "known_U_value",
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
        schema="core",
    )
    op.alter_column(
        "ceiling",
        "insulated_wall",
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
        schema="core",
    )
    op.alter_column(
        "ceiling",
        "insulated_non_heated_exterior_wall",
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
        schema="core",
    )
    op.alter_column(
        "ceiling",
        "insulated_heated_non_heated_wall",
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
        schema="core",
    )
    # ### end Alembic commands ###