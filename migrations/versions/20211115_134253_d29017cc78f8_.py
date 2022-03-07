"""empty message

Revision ID: d29017cc78f8
Revises: a3af4bff64a5
Create Date: 2021-11-15 13:42:53.430242

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd29017cc78f8'
down_revision = 'a3af4bff64a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('copro',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('mission_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('address_1_id', sa.Integer(), nullable=True),
                    sa.Column('address_2_id', sa.Integer(), nullable=True),
                    sa.Column('user_in_charge_id', sa.Integer(), nullable=True),
                    sa.Column('mixed_copro', sa.Boolean(), nullable=True),
                    sa.Column('priority_copro', sa.Boolean(), nullable=True),
                    sa.Column('horizontal_copro', sa.Boolean(), nullable=True),
                    sa.Column('copro_registry_number', sa.Integer(), nullable=True),
                    sa.Column('copro_creation_date', sa.Date(), nullable=True),
                    sa.Column('is_member_s1_s2', sa.Boolean(), nullable=True),
                    sa.Column('is_member_association', sa.Boolean(), nullable=True),
                    sa.Column('nb_lots', sa.Integer(), nullable=True),
                    sa.Column('nb_co_owners', sa.Integer(), nullable=True),
                    sa.Column('nb_sub_lots', sa.Integer(), nullable=True),
                    sa.Column('percentage_lots_to_habitation', sa.Float(), nullable=True),
                    sa.Column('percentage_tantiemes_to_habitation', sa.Float(), nullable=True),
                    sa.Column('contract_end_date', sa.Date(), nullable=True),
                    sa.Column('closing_accounts_date', sa.Date(), nullable=True),
                    sa.Column('last_assembly_date', sa.Date(), nullable=True),
                    sa.Column('percentage_attending_tantiemes', sa.Float(), nullable=True),
                    sa.Column('percentage_attending_co_owners', sa.Float(), nullable=True),
                    sa.Column('institutional_landlords_presence', sa.Boolean(), nullable=True),
                    sa.Column('charges_last_year', sa.Float(), nullable=True),
                    sa.Column('provisional_budget_last_assembly', sa.Float(), nullable=True),
                    sa.Column('average_charges_per_quarter_per_lot', sa.Float(), nullable=True),
                    sa.Column('construction_time', sa.String(length=255), nullable=True),
                    sa.Column('pmr', sa.Boolean(), nullable=True),
                    sa.Column('igh', sa.Boolean(), nullable=True),
                    sa.Column('external_spaces', sa.Boolean(), nullable=True),
                    sa.Column('underground_parking', sa.Boolean(), nullable=True),
                    sa.Column('aerial_parking', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['address_1_id'], ['core.address.id'],
                                            name=op.f('fk_copro_address_1_id_address')),
                    sa.ForeignKeyConstraint(['address_2_id'], ['core.address.id'],
                                            name=op.f('fk_copro_address_2_id_address')),
                    sa.ForeignKeyConstraint(['mission_id'], ['core.mission.id'],
                                            name=op.f('fk_copro_mission_id_mission')),
                    sa.ForeignKeyConstraint(['user_in_charge_id'], ['core.user.id'],
                                            name=op.f('fk_copro_user_in_charge_id_user')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_copro')),
                    schema='core'
                    )
    op.create_table('cadastre',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('copro_id', sa.Integer(), nullable=False),
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(['copro_id'], ['core.copro.id'], name=op.f('fk_cadastre_copro_id_copro')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_cadastre')),
                    schema='core'
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cadastre', schema='core')
    op.drop_table('copro', schema='core')
    # ### end Alembic commands ###
