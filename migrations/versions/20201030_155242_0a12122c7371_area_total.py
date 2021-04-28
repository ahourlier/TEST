"""area total

Revision ID: 0a12122c7371
Revises: f7d30b0759f9
Create Date: 2020-10-30 15:52:42.939767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0a12122c7371"
down_revision = "f7d30b0759f9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("area", sa.Column("total", sa.Float(), nullable=True), schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("area", "total", schema="core")
    # ### end Alembic commands ###
