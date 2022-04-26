"""empty message

Revision ID: 5a07effd417d
Revises: fd623e7bb59d
Create Date: 2022-02-24 09:08:24.234110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a07effd417d'
down_revision = 'fd623e7bb59d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('person', 'address_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('person', 'address_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='core')
    # ### end Alembic commands ###