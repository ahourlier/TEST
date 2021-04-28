"""accommodation case type

Revision ID: 636ab59b1524
Revises: 1e369e4f68a7
Create Date: 2020-07-01 16:31:31.613892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "636ab59b1524"
down_revision = "1e369e4f68a7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accommodation",
        sa.Column("case_type", sa.String(length=255), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("accommodation", "case_type", schema="core")
    # ### end Alembic commands ###
