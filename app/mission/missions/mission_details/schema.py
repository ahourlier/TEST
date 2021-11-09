from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.mission.missions.mission_details.model import MissionDetail
from app.mission.missions.mission_details.partner.schema import PartnerSchema
from app.admin.subcontractor.schema import SubcontractorSchema
from app.mission.missions.mission_details.elect.schema import ElectSchema


class MissionDetailSchema(SQLAlchemyAutoSchema):
    mission_id = fields.Integer(dump_only=True)
    partners = fields.List(fields.Nested(PartnerSchema()), dump_only=True)
    subcontractors = fields.List(fields.Nested(SubcontractorSchema()), dump_only=True)
    elects = fields.List(fields.Nested(ElectSchema()), dump_only=True)

    class Meta:
        model = MissionDetail
        include_fk = True
        unknown = EXCLUDE
