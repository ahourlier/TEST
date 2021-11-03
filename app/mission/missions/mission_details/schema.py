from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.mission.missions.mission_details.model import MissionDetail


class MissionDetailSchema(SQLAlchemyAutoSchema):
    mission_id = fields.Integer(dump_only=True)

    class Meta:
        model = MissionDetail
        include_fk = True
        unknown = EXCLUDE
