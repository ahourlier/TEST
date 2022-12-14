"""empty message

Revision ID: 376cb90e6ca9
Revises: 5e7de5dfd5be
Create Date: 2022-02-10 09:26:30.194248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '376cb90e6ca9'
down_revision = '5e7de5dfd5be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requester', sa.Column('cadastral_reference', sa.String(length=255), nullable=True), schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requester', 'cadastral_reference', schema='core')
    # ### end Alembic commands ###
