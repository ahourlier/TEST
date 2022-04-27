"""empty message

Revision ID: b1b17cb27d52
Revises: 080cb19518ad
Create Date: 2022-04-27 11:38:19.979825

"""
from datetime import datetime
from alembic import op
from sqlalchemy.orm import Session
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b1b17cb27d52'
down_revision = '080cb19518ad'
branch_labels = None
depends_on = None

versions = postgresql.ENUM('INDIVIDUEL', 'COPROPRIETE', name='versiontype')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    versions.create(bind=bind)

    session = Session(bind=bind)
    # Reset permissions with type version
    session.execute("DELETE FROM core.permission;")

    op.add_column('permission', sa.Column('applied_to', sa.Enum('V1', 'V2', name='versiontype'), nullable=False), schema='core')
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    op.drop_constraint(constraint_name=op.f("pk_permission"), table_name='permission', schema='core', type_="unique")
    op.create_unique_constraint(op.f("pk_permission"), columns=["entity", "action", "role_id", "applied_to"], schema='core', table_name='permission')

    session.execute(
        "INSERT INTO core.permission (created_at, updated_at, entity, action, role_id, applied_to) VALUES "
        f"('{now}', '{now}', \'agency\', \'create\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'agency\', \'delete\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'agency\', \'read\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'agency\', \'update\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'antenna\', \'create\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'antenna\', \'delete\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'antenna\', \'read\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'antenna\', \'update\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder\', \'create\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder\', \'delete\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder\', \'update\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'user\', \'create\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'user\', \'delete\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'user\', \'read\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'user\', \'update\', \'admin\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'client\', \'read\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'project\', \'create\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'project\', \'delete\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'project\', \'read\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'project\', \'update\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'requester\', \'create\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'requester\', \'delete\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'requester\', \'read\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'requester\', \'update\', \'contributor\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'client\', \'create\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'client\', \'delete\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'client\', \'update\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder\', \'read\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder_mission\', \'create\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder_mission\', \'delete\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder_mission\', \'read\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'funder_mission\', \'update\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'mission\', \'create\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'mission\', \'delete\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'mission\', \'read\', \'manager\', \'INDIVIDUEL\'),"
        f"('{now}', '{now}', \'mission\', \'update\', \'manager\', \'INDIVIDUEL\')"
    )

    session.execute(
        "INSERT INTO core.permission (created_at, updated_at, entity, action, role_id, applied_to) VALUES "
        f"('{now}', '{now}', \'agency\',	\'create\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'agency\',	\'delete\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'agency\',	\'read\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'agency\',	\'update\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'antenna\',	\'create\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'antenna\',	\'delete\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'antenna\',	\'read\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'antenna\',	\'update\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'user\',	\'create\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'user\',	\'delete\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'user\',	\'read\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'user\',	\'update\',	\'admin\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_task\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_task\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_task\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_task\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_task\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_task\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_task\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_task\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_task\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_task\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_task\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_task\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission\',	\'create\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission\',	\'update\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission\',	\'delete\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_details\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_details\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_details\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_details\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_event\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_event\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_event\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_event\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_import\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_import\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_import\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'mission_import\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_task\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_task\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_task\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_task\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'read\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'create\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'update\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'delete\',	\'contributor\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'client\',	\'update\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'client\',	\'read\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'client\',	\'delete\',	\'manager\', \'COPROPRIETE\'),"
        f"('{now}', '{now}', \'client\',	\'create\',	\'manager\', \'COPROPRIETE\')"
        
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permission', 'applied_to', schema='core')
    bind = op.get_bind()
    session = Session(bind=bind)
    # Reset permissions without type
    session.execute("DELETE FROM core.permission;")

    #op.drop_constraint(constraint_name=op.f("pk_permission"), table_name='permission', schema='core', type_="unique")
    op.create_unique_constraint(op.f("pk_permission"), columns=["entity", "action", "role_id"], schema='core', table_name='permission')

    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
   
    session.execute(
        "INSERT INTO core.permission (created_at, updated_at, entity, action, role_id) VALUES "
        f"('{now}', '{now}', \'agency\',	\'create\',	\'admin\'),"
        f"('{now}', '{now}', \'agency\',	\'delete\',	\'admin\'),"
        f"('{now}', '{now}', \'agency\',	\'read\',	\'admin\'),"
        f"('{now}', '{now}', \'agency\',	\'update\',	\'admin\'),"
        f"('{now}', '{now}', \'antenna\',	\'create\',	\'admin\'),"
        f"('{now}', '{now}', \'antenna\',	\'delete\',	\'admin\'),"
        f"('{now}', '{now}', \'antenna\',	\'read\',	\'admin\'),"
        f"('{now}', '{now}', \'antenna\',	\'update\',	\'admin\'),"
        f"('{now}', '{now}', \'funder\',	\'update\',	\'admin\'),"
        f"('{now}', '{now}', \'funder\',	\'delete\',	\'admin\'),"
        f"('{now}', '{now}', \'funder\',	\'create\',	\'admin\'),"
        f"('{now}', '{now}', \'user\',	\'create\',	\'admin\'),"
        f"('{now}', '{now}', \'user\',	\'delete\',	\'admin\'),"
        f"('{now}', '{now}', \'user\',	\'read\',	\'admin\'),"
        f"('{now}', '{now}', \'user\',	\'update\',	\'admin\'),"
        f"('{now}', '{now}', \'building\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'building\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'building\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'building\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_task\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_task\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_task\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_task\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'building_thematic\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_task\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_task\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_task\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_task\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'copro_thematic\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_task\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_task\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_task\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_task\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'lot_thematic\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission\',	\'create\',	\'manager\'),"
        f"('{now}', '{now}', \'mission\',	\'update\',	\'manager\'),"
        f"('{now}', '{now}', \'mission\',	\'delete\',	\'manager\'),"
        f"('{now}', '{now}', \'mission_details\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_details\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_details\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_details\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_event\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_event\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_event\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_event\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_import\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_import\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_import\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'mission_import\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'project\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'project\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'project\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'project\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'requester\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'requester\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'requester\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'requester\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_task\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_task\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_task\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_task\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'sc_thematic\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'read\',	\'contributor\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'create\',	\'contributor\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'update\',	\'contributor\'),"
        f"('{now}', '{now}', \'subcontractor\',	\'delete\',	\'contributor\'),"
        f"('{now}', '{now}', \'client\',	\'update\',	\'manager\'),"
        f"('{now}', '{now}', \'client\',	\'read\',	\'manager\'),"
        f"('{now}', '{now}', \'client\',	\'delete\',	\'manager\'),"
        f"('{now}', '{now}', \'client\',	\'create\',	\'manager\'),"
        f"('{now}', '{now}', \'funder\',	\'read\',	\'manager\'),"
        f"('{now}', '{now}', \'funder_mission\',	\'create\',	\'manager\'),"
        f"('{now}', '{now}', \'funder_mission\',	\'delete\',	\'manager\'),"
        f"('{now}', '{now}', \'funder_mission\',	\'read\',	\'manager\'),"
        f"('{now}', '{now}', \'funder_mission\',	\'update\',	\'manager\')"
    )

    versions.drop(bind=bind)
    # ### end Alembic commands ###