"""empty message

Revision ID: 474c6baff12d
Revises: 919538d32015
Create Date: 2021-11-16 17:27:51.768469

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '474c6baff12d'
down_revision = '919538d32015'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('syndic',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('copro_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('type', sa.String(length=255), nullable=True),
                    sa.Column('manager_name', sa.String(length=255), nullable=True),
                    sa.Column('manager_address_id', sa.Integer(), nullable=True),
                    sa.Column('manager_email', sa.String(length=255), nullable=True),
                    sa.Column('comment', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['copro_id'], ['core.copro.id'], name=op.f('fk_syndic_copro_id_copro')),
                    sa.ForeignKeyConstraint(['manager_address_id'], ['core.address.id'],
                                            name=op.f('fk_syndic_manager_address_id_address')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_syndic')),
                    schema='core'
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('syndic', schema='core')
    # ### end Alembic commands ###
