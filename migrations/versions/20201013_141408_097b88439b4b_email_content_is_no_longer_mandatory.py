"""email content is no longer mandatory

Revision ID: 097b88439b4b
Revises: b691f0d07a41
Create Date: 2020-10-13 14:14:08.570149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "097b88439b4b"
down_revision = "c0141b8a6d1f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "email", "content", existing_type=sa.TEXT(), nullable=True, schema="core"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "email", "content", existing_type=sa.TEXT(), nullable=False, schema="core"
    )
    # ### end Alembic commands ###