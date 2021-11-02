from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE

from app.mission.missions.mission_details.model import MissionDetail


class MissionDetailSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = MissionDetail
        include_fk = True
        unknown = EXCLUDE
