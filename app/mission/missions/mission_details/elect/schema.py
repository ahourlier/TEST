from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.mission.missions.mission_details.elect import Elect


class ElectSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Elect
        include_fk = True
        unknown = EXCLUDE


class ElectUpdateSchema(SQLAlchemyAutoSchema):
    mission_details_id = fields.Integer(dump_only=True)

    class Meta:
        model = Elect
        include_fk = True
        unknown = EXCLUDE
