"""quotes_modified_flag

Revision ID: fae89d89e094
Revises: e24ca003fb02
Create Date: 2020-06-17 16:51:34.634719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fae89d89e094"
down_revision = "e24ca003fb02"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "simulation",
        sa.Column("quotes_modified", sa.Boolean(), nullable=True),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("simulation", "quotes_modified", schema="core")
    # ### end Alembic commands ###
