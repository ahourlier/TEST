"""empty message

Revision ID: 544adbbcc18e
Revises: 7460f8230870
Create Date: 2022-06-08 15:01:57.738216

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '544adbbcc18e'
down_revision = '7460f8230870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('financial_device',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mission_details_id', sa.Integer(), nullable=False),
    sa.Column('mandate_account_type', sa.String(length=255), nullable=True),
    sa.Column('organization_funds_provider', sa.String(length=255), nullable=True),
    sa.Column('bank_account_name', sa.String(length=255), nullable=True),
    sa.Column('bank_name', sa.String(length=255), nullable=True),
    sa.Column('agreement_signature_date', sa.Date(), nullable=True),
    sa.Column('amendment_signature_date', sa.Date(), nullable=True),
    sa.Column('convention_number', sa.String(length=255), nullable=True),
    sa.Column('initiale_envelop', sa.Integer(), nullable=True),
    sa.Column('complementary_envelop', sa.Integer(), nullable=True),
    sa.Column('internal_audit_date', sa.Date(), nullable=True),
    sa.Column('external_audit_date', sa.Date(), nullable=True),
    sa.Column('funds_return_date', sa.Date(), nullable=True),
    sa.Column('amount_returned', sa.Integer(), nullable=True),
    sa.Column('closing_date', sa.Date(), nullable=True),
    sa.Column('transfer_circuit_validation', sa.String(length=500), nullable=True),
    sa.Column('operating_details', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['mission_details_id'], ['core.mission_detail.id'], name=op.f('fk_financial_device_mission_details_id_mission_detail')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_financial_device')),
    schema='core'
    )
    op.drop_column('mission_detail', 'internal_audit_date', schema='core')
    op.drop_column('mission_detail', 'operating_details', schema='core')
    op.drop_column('mission_detail', 'closing_date', schema='core')
    op.drop_column('mission_detail', 'convention_number', schema='core')
    op.drop_column('mission_detail', 'organization_funds_provider', schema='core')
    op.drop_column('mission_detail', 'agreement_signature_date', schema='core')
    op.drop_column('mission_detail', 'amendment_signature_date', schema='core')
    op.drop_column('mission_detail', 'bank_account_name', schema='core')
    op.drop_column('mission_detail', 'external_audit_date', schema='core')
    op.drop_column('mission_detail', 'financial_device_used', schema='core')
    op.drop_column('mission_detail', 'bank_name', schema='core')
    op.drop_column('mission_detail', 'mandate_account_type', schema='core')
    op.drop_column('mission_detail', 'complementary_envelop', schema='core')
    op.drop_column('mission_detail', 'funds_return_date', schema='core')
    op.drop_column('mission_detail', 'initiale_envelop', schema='core')
    op.drop_column('mission_detail', 'transfer_circuit_validation', schema='core')
    op.drop_column('mission_detail', 'amount_returned', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mission_detail', sa.Column('amount_returned', sa.INTEGER(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('transfer_circuit_validation', sa.VARCHAR(length=500), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('initiale_envelop', sa.INTEGER(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('funds_return_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('complementary_envelop', sa.INTEGER(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('mandate_account_type', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('bank_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('financial_device_used', sa.BOOLEAN(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('external_audit_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('bank_account_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('amendment_signature_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('agreement_signature_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('organization_funds_provider', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('convention_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('closing_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('operating_details', sa.VARCHAR(length=500), autoincrement=False, nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('internal_audit_date', sa.DATE(), autoincrement=False, nullable=True), schema='core')
    op.drop_table('financial_device', schema='core')
    # ### end Alembic commands ###
