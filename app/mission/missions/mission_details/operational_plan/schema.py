from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE

from app.mission.missions.mission_details.operational_plan.model import OperationalPlan


class OperationalPlanSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = OperationalPlan
        include_fk = True
        unknown = EXCLUDE
