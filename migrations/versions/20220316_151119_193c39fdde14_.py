"""empty message

Revision ID: 193c39fdde14
Revises: 83f2f6a8ea59
Create Date: 2022-03-16 15:11:19.767163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '193c39fdde14'
down_revision = '83f2f6a8ea59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('copro', sa.Column('syndic_name', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_type', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_contract_date', sa.Date(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_manager_name', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_manager_email', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_comment', sa.Text(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('syndic_manager_address_id', sa.Integer(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_name', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_type', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_contract_date', sa.Date(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_manager_name', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_manager_email', sa.String(length=255), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_comment', sa.Text(), nullable=True), schema='core')
    op.add_column('copro', sa.Column('admin_manager_address_id', sa.Integer(), nullable=True), schema='core')
    op.create_foreign_key(op.f('fk_copro_syndic_manager_address_id_address'), 'copro', 'address', ['syndic_manager_address_id'], ['id'], source_schema='core', referent_schema='core')
    op.create_foreign_key(op.f('fk_copro_admin_manager_address_id_address'), 'copro', 'address', ['admin_manager_address_id'], ['id'], source_schema='core', referent_schema='core')
    op.drop_constraint('fk_syndic_copro_id_copro', 'syndic', schema='core', type_='foreignkey')
    op.drop_column('syndic', 'copro_id', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('syndic', sa.Column('copro_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='core')
    op.create_foreign_key('fk_syndic_copro_id_copro', 'syndic', 'copro', ['copro_id'], ['id'], source_schema='core', referent_schema='core')
    op.drop_constraint(op.f('fk_copro_admin_manager_address_id_address'), 'copro', schema='core', type_='foreignkey')
    op.drop_constraint(op.f('fk_copro_syndic_manager_address_id_address'), 'copro', schema='core', type_='foreignkey')
    op.drop_column('copro', 'admin_manager_address_id', schema='core')
    op.drop_column('copro', 'admin_comment', schema='core')
    op.drop_column('copro', 'admin_manager_email', schema='core')
    op.drop_column('copro', 'admin_manager_name', schema='core')
    op.drop_column('copro', 'admin_contract_date', schema='core')
    op.drop_column('copro', 'admin_type', schema='core')
    op.drop_column('copro', 'admin_name', schema='core')
    op.drop_column('copro', 'syndic_manager_address_id', schema='core')
    op.drop_column('copro', 'syndic_comment', schema='core')
    op.drop_column('copro', 'syndic_manager_email', schema='core')
    op.drop_column('copro', 'syndic_manager_name', schema='core')
    op.drop_column('copro', 'syndic_contract_date', schema='core')
    op.drop_column('copro', 'syndic_type', schema='core')
    op.drop_column('copro', 'syndic_name', schema='core')
    # ### end Alembic commands ###