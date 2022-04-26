"""empty message

Revision ID: 16e3807f7b28
Revises: 403a79d79190
Create Date: 2020-04-15 13:52:36.377291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16e3807f7b28"
down_revision = "403a79d79190"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contact",
        sa.Column("address", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project", sa.Column("closed", sa.Boolean(), nullable=True), schema="core"
    )
    op.add_column(
        "project",
        sa.Column("closure_motive", sa.String(length=255), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("date_advice_meet", sa.Date(), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("date_control_meet", sa.Date(), nullable=True),
        schema="core",
    )
    op.add_column(
        "project",
        sa.Column("notes", sa.String(length=2083), nullable=True),
        schema="core",
    )
    op.add_column(
        "project", sa.Column("urgent_visit", sa.Boolean(), nullable=True), schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "urgent_visit", schema="core")
    op.drop_column("project", "notes", schema="core")
    op.drop_column("project", "date_control_meet", schema="core")
    op.drop_column("project", "date_advice_meet", schema="core")
    op.drop_column("project", "closure_motive", schema="core")
    op.drop_column("project", "closed", schema="core")
    op.drop_column("contact", "address", schema="core")
    # ### end Alembic commands ###