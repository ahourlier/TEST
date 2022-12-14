"""mission drive init

Revision ID: e49debd57ed0
Revises: 1eeba4e99024
Create Date: 2021-03-12 11:12:13.261477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e49debd57ed0'
down_revision = '1eeba4e99024'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mission', sa.Column('drive_init', sa.String(length=255), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mission', 'drive_init', schema='core')
    # ### end Alembic commands ###
