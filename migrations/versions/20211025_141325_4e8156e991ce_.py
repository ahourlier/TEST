"""empty message

Revision ID: 4e8156e991ce
Revises: b9f54bb64372
Create Date: 2021-10-25 14:13:24.401869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e8156e991ce'
down_revision = 'b16e2c5183aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('preferred_app',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('preferred_app', sa.String(length=11), nullable=True),
    sa.Column('first_connection', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_preferred_app')),
    schema='core'
    )
    op.add_column('user', sa.Column('preferred_app_id', sa.Integer(), nullable=True), schema='core')
    op.create_foreign_key(op.f('fk_user_preferred_app_id_preferred_app'), 'user', 'preferred_app', ['preferred_app_id'], ['id'], source_schema='core', referent_schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_user_preferred_app_id_preferred_app'), 'user', schema='core', type_='foreignkey')
    op.drop_column('user', 'preferred_app_id', schema='core')
    op.drop_table('preferred_app', schema='core')
    # ### end Alembic commands ###