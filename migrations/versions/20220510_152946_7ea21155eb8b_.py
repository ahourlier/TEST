"""empty message

Revision ID: 7ea21155eb8b
Revises: 4c582035b38f
Create Date: 2022-05-10 15:29:46.428972

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ea21155eb8b'
down_revision = '4c582035b38f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('phone_number', 'country_code',
               existing_type=sa.VARCHAR(length=3),
               nullable=True,
               schema='core')
    op.alter_column('phone_number', 'national',
               existing_type=sa.VARCHAR(length=128),
               nullable=True,
               schema='core')
    op.alter_column('phone_number', 'international',
               existing_type=sa.VARCHAR(length=128),
               nullable=True,
               schema='core')
    op.alter_column('phone_number', 'resource_type',
               existing_type=sa.VARCHAR(length=128),
               nullable=True,
               schema='core')
    op.alter_column('phone_number', 'resource_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('phone_number', 'resource_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='core')
    op.alter_column('phone_number', 'resource_type',
               existing_type=sa.VARCHAR(length=128),
               nullable=False,
               schema='core')
    op.alter_column('phone_number', 'international',
               existing_type=sa.VARCHAR(length=128),
               nullable=False,
               schema='core')
    op.alter_column('phone_number', 'national',
               existing_type=sa.VARCHAR(length=128),
               nullable=False,
               schema='core')
    op.alter_column('phone_number', 'country_code',
               existing_type=sa.VARCHAR(length=3),
               nullable=False,
               schema='core')
    # ### end Alembic commands ###
