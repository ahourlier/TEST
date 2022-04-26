"""fix year_nb type

Revision ID: 127ff03c0bf3
Revises: c43dc508a276
Create Date: 2020-04-17 12:03:26.787485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "127ff03c0bf3"
down_revision = "5e81085eced8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accomodation",
        sa.Column("year_vacant_nb", sa.Integer(), nullable=True),
        schema="core",
    )
    op.drop_column("accomodation", "year_nb", schema="core")
    op.drop_column("client", "phone_number", schema="core")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "client",
        sa.Column(
            "phone_number", sa.VARCHAR(length=50), autoincrement=False, nullable=True
        ),
        schema="core",
    )
    op.add_column(
        "accomodation",
        sa.Column("year_nb", sa.DATE(), autoincrement=False, nullable=True),
        schema="core",
    )
    op.drop_column("accomodation", "year_vacant_nb", schema="core")
    # ### end Alembic commands ###