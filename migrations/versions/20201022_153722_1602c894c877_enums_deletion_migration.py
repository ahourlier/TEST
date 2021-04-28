"""enums deletion migration

Revision ID: 1602c894c877
Revises: 097b88439b4b
Create Date: 2020-10-22 15:37:22.352718

"""
from alembic import op
from sqlalchemy.orm import Session
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm, MetaData, Table

from app.mission.missions import Mission
from app.referential.enums import AppEnum

revision = "1602c894c877"
down_revision = "097b88439b4b"
branch_labels = None
depends_on = None

enum_kinds_to_set_editable = [
    "ProjectContactSource",
    "ProjectRequesterResourceCategory",
    "ProjectRequesterProfessionType",
    "ProjectCaseType",
    "ProjectWorksType",
    "ProjectClosureMotiveType",
    "ProjectAccommodationType",
    "FunderType",
    "ProjectAccommodationTypology",
    "ProjectAccommodationRentTypeAfterRenovation",
    "ProjectAccommodationAccess",
    "ProjectAdaptationAnalysis",
    "ProjectHeatingAnalysis",
    "ProjectHeatingRecommendation",
    "ProjectAdaptationRecommendation",
    "ProjectTechnicalRecommendation",
    "ProjectTechnicalAnalysis",
]


def upgrade():
    bind = op.get_bind()
    meta = MetaData(bind=bind, schema="core")
    meta.reflect(only=("enum",))
    session = Session(bind=bind)

    for enum_kind in enum_kinds_to_set_editable:
        query = f"UPDATE core.enum SET private=FALSE WHERE kind = '{enum_kind}';"
        session.execute(query)


def downgrade():
    bind = op.get_bind()
    meta = MetaData(bind=bind, schema="core")
    meta.reflect(only=("enum",))
    session = Session(bind=bind)

    for enum_kind in enum_kinds_to_set_editable:
        query = f"UPDATE core.enum SET private=TRUE WHERE kind = '{enum_kind}';"
        session.execute(query)
