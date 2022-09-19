"""to is no longer required

Revision ID: 5a9994bed9ec
Revises: 8b5fca25333a
Create Date: 2020-09-08 15:59:43.090559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5a9994bed9ec"
down_revision = "8b5fca25333a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "email",
        "to",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=255)),
        nullable=True,
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "email",
        "to",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=255)),
        nullable=False,
        schema="core",
    )
    # ### end Alembic commands ###