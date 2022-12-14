"""Project type can be null

Revision ID: 981991a1a4ce
Revises: 09703cacc1ac
Create Date: 2020-05-06 12:11:36.340586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "981991a1a4ce"
down_revision = "09703cacc1ac"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "project",
        "type",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "project",
        "type",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
        schema="core",
    )
    # ### end Alembic commands ###
