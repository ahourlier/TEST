"""perrenoud enums

Revision ID: 1ad5a0600b9c
Revises: 1602c894c877
Create Date: 2020-10-23 17:59:06.488896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1ad5a0600b9c"
down_revision = "1602c894c877"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "perrenoud_enum",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("kind", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_perrenoud_enum")),
        schema="core",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("perrenoud_enum", schema="core")
    # ### end Alembic commands ###
