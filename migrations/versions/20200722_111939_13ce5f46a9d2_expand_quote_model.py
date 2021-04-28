"""expand Quote model

Revision ID: 13ce5f46a9d2
Revises: 31c79a1bb808
Create Date: 2020-07-22 11:19:39.717341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "13ce5f46a9d2"
down_revision = "31c79a1bb808"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "quote",
        sa.Column("common_eligible_amount", sa.Float(), nullable=True),
        schema="core",
    )
    op.add_column(
        "quote",
        sa.Column("common_note", sa.String(length=2083), nullable=True),
        schema="core",
    )
    op.add_column(
        "quote",
        sa.Column("common_price_excl_tax", sa.Float(), nullable=True),
        schema="core",
    )
    op.add_column(
        "quote",
        sa.Column("common_price_incl_tax", sa.Float(), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quote", "common_price_incl_tax", schema="core")
    op.drop_column("quote", "common_price_excl_tax", schema="core")
    op.drop_column("quote", "common_note", schema="core")
    op.drop_column("quote", "common_eligible_amount", schema="core")
    # ### end Alembic commands ###
