"""empty message

Revision ID: dac74fa98bf8
Revises: cd1b8543d53a
Create Date: 2022-03-24 13:29:15.229119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dac74fa98bf8'
down_revision = 'cd1b8543d53a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lot_occupants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['core.lot.id'], name=op.f('fk_lot_occupants_lot_id_lot')),
    sa.ForeignKeyConstraint(['person_id'], ['core.person.id'], name=op.f('fk_lot_occupants_person_id_person')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lot_occupants')),
    schema='core'
    )
    op.create_table('lot_owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['core.lot.id'], name=op.f('fk_lot_owners_lot_id_lot')),
    sa.ForeignKeyConstraint(['owner_id'], ['core.person.id'], name=op.f('fk_lot_owners_owner_id_person')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lot_owners')),
    schema='core'
    )
    op.drop_table('lot_person', schema='core')
    op.drop_constraint('fk_lot_owner_id_person', 'lot', schema='core', type_='foreignkey')
    op.drop_column('lot', 'owner_id', schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lot', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='core')
    op.create_foreign_key('fk_lot_owner_id_person', 'lot', 'person', ['owner_id'], ['id'], source_schema='core', referent_schema='core')
    op.create_table('lot_person',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('core.lot_person_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('person_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lot_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['core.lot.id'], name='fk_lot_person_lot_id_lot'),
    sa.ForeignKeyConstraint(['person_id'], ['core.person.id'], name='fk_lot_person_person_id_person'),
    sa.PrimaryKeyConstraint('id', name='pk_lot_person'),
    schema='core'
    )
    op.drop_table('lot_owners', schema='core')
    op.drop_table('lot_occupants', schema='core')
    # ### end Alembic commands ###