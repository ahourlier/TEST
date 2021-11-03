from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.mission.missions.mission_details.subjob.model import Subjob


class SubjobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subjob
        include_fk = True
        unknown = EXCLUDE
