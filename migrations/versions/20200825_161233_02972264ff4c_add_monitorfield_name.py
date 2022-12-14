"""add_monitorfield_name

Revision ID: 02972264ff4c
Revises: 205c27a03e8b
Create Date: 2020-08-25 16:12:33.427047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "02972264ff4c"
down_revision = "205c27a03e8b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "monitor_field",
        sa.Column("name", sa.String(length=255), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("monitor_field", "name", schema="core")
    # ### end Alembic commands ###
