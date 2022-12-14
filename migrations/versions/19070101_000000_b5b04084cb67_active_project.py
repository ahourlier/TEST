"""active_project

Revision ID: b5b04084cb67
Revises: d467567d9b98
Create Date: 2020-04-16 10:23:43.586676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5b04084cb67"
down_revision = "d467567d9b98"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project",
        sa.Column("active", sa.Boolean(create_constraint=False), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "active", schema="core")
    # ### end Alembic commands ###
