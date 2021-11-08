"""empty message

Revision ID: 5fcbe25b6734
Revises: 9a8e3b37e92b
Create Date: 2021-10-29 16:05:48.021618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5fcbe25b6734'
down_revision = '9a8e3b37e92b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mission_detail',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('mission_id', sa.Integer(), nullable=False),
                    sa.Column('previous_running_meeting', sa.Date(), nullable=True),
                    sa.Column('market_number', sa.Integer(), nullable=True),
                    sa.Column('os_signing_date', sa.Date(), nullable=True),
                    sa.Column('has_sub_contractor', sa.Boolean(), nullable=True),
                    sa.Column('billing_type_tf', sa.String(length=255), nullable=True),
                    sa.Column('billing_type_tc', sa.String(length=255), nullable=True),
                    sa.Column('purchase_order_market', sa.Boolean(), nullable=True),
                    sa.Column('smq_starting_meeting', sa.Date(), nullable=True),
                    sa.Column('smq_engagement_meeting', sa.Date(), nullable=True),
                    sa.Column('smq_previous_meeting', sa.Date(), nullable=True),
                    sa.ForeignKeyConstraint(['mission_id'], ['core.mission.id'],
                                            name=op.f('fk_mission_detail_mission_id_mission')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_mission_detail')),
                    sa.UniqueConstraint('mission_id', name=op.f('uq_mission_detail_mission_id')),
                    schema='core'
                    )
    op.create_table('job',
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('value', name=op.f('pk_job')),
                    schema='core'
                    )
    op.create_table('subjob',
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('value', name=op.f('pk_subjob')),
                    schema='core'
                    )
    op.create_table('operational_plan',
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('value', name=op.f('pk_operational_plan')),
                    schema='core'
                    )
    op.add_column('mission_detail', sa.Column('operational_plan', sa.String(length=255), nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('job', sa.String(length=255), nullable=True), schema='core')
    op.add_column('mission_detail', sa.Column('subjob', sa.String(length=255), nullable=True), schema='core')
    op.create_foreign_key(op.f('fk_mission_detail_job_job'), 'mission_detail', 'job', ['job'], ['value'],
                          source_schema='core', referent_schema='core')
    op.create_foreign_key(op.f('fk_mission_detail_operational_plan_operational_plan'), 'mission_detail',
                          'operational_plan', ['operational_plan'], ['value'], source_schema='core',
                          referent_schema='core')
    op.create_foreign_key(op.f('fk_mission_detail_subjob_subjob'), 'mission_detail', 'subjob', ['subjob'], ['value'],
                          source_schema='core', referent_schema='core')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mission_detail', schema='core')
    op.drop_table('operational_plan', schema='core')
    op.drop_table('subjob', schema='core')
    op.drop_table('job', schema='core')
    # ### end Alembic commands ###
