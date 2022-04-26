"""split_addresses

Revision ID: ee7d8b0c032c
Revises: 8290571869e3
Create Date: 2020-10-05 15:18:01.608377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ee7d8b0c032c"
down_revision = "8290571869e3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project",
        sa.Column("address_code", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_complement", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_latitude", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_location", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_longitude", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_number", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("address_street", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_code", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_complement", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_latitude", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_location", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_longitude", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_number", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "requester",
        sa.Column("address_street", sa.String(length=255), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("requester", "address_street", schema="core")
    op.drop_column("requester", "address_number", schema="core")
    op.drop_column("requester", "address_longitude", schema="core")
    op.drop_column("requester", "address_location", schema="core")
    op.drop_column("requester", "address_latitude", schema="core")
    op.drop_column("requester", "address_complement", schema="core")
    op.drop_column("requester", "address_code", schema="core")
    op.drop_column("project", "address_street", schema="core")
    op.drop_column("project", "address_number", schema="core")
    op.drop_column("project", "address_longitude", schema="core")
    op.drop_column("project", "address_location", schema="core")
    op.drop_column("project", "address_latitude", schema="core")
    op.drop_column("project", "address_complement", schema="core")
    op.drop_column("project", "address_code", schema="core")
    # ### end Alembic commands ###