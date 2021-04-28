from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Mission
from ..teams.schema import TeamSchema
from ...admin.agencies import AgencySchema
from ...admin.antennas import AntennaSchema
from ...admin.clients.schema import ClientSchema
from ...common.schemas import PaginatedSchema, DocumentSchema


class MissionSchema(SQLAlchemyAutoSchema):
    agency = fields.Nested(AgencySchema())
    antenna = fields.Nested(AntennaSchema())
    client = fields.Nested(ClientSchema())
    code_name = fields.String(dump_only=True)

    class Meta:
        model = Mission
        include_fk = True
        unknown = EXCLUDE


class MissionPaginatedSchema(PaginatedSchema):
    items = fields.Nested(MissionSchema(), many=True, dump_only=True)


class MissionDocumentSchema(DocumentSchema):
    pass
