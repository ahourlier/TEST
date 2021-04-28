"""project drive init

Revision ID: aded195b5e2a
Revises: e49debd57ed0
Create Date: 2021-03-12 11:24:42.461639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aded195b5e2a'
down_revision = 'e49debd57ed0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('drive_init', sa.String(length=255), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'drive_init', schema='core')
    # ### end Alembic commands ###
