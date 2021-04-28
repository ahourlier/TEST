"""add html_content field to comment model

Revision ID: 4d99630088e9
Revises: ca9dcb8eb5e2
Create Date: 2020-09-08 16:49:37.928630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4d99630088e9"
down_revision = "ca9dcb8eb5e2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comment", sa.Column("html_content", sa.Text(), nullable=True), schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("comment", "html_content", schema="core")
    # ### end Alembic commands ###
