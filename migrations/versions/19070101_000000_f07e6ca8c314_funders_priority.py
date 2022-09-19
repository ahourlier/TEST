"""funders priority

Revision ID: f07e6ca8c314
Revises: 938ed27829b8
Create Date: 2020-05-15 09:01:45.226329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f07e6ca8c314"
down_revision = "938ed27829b8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "funder", sa.Column("priority", sa.Integer(), nullable=True), schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("funder", "priority", schema="core")
    # ### end Alembic commands ###