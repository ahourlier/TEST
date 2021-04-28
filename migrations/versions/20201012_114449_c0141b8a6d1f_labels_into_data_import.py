"""labels into data import

Revision ID: c0141b8a6d1f
Revises: 793c8785df99
Create Date: 2020-10-12 11:44:49.415113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0141b8a6d1f"
down_revision = "793c8785df99"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "data_import", sa.Column("labels", sa.Text(), nullable=True), schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("data_import", "labels", schema="core")
    # ### end Alembic commands ###
