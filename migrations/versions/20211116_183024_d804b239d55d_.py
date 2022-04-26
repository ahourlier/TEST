"""empty message

Revision ID: d804b239d55d
Revises: 474c6baff12d
Create Date: 2021-11-16 18:30:24.525641

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd804b239d55d'
down_revision = '474c6baff12d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('president',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('copro_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('email_address', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['copro_id'], ['core.copro.id'], name=op.f('fk_president_copro_id_copro')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_president')),
                    schema='core'
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('president', schema='core')
    # ### end Alembic commands ###