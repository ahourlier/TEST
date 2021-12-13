from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Mission
from ..teams.schema import TeamSchema
from ...admin.agencies import AgencySchema
from ...admin.antennas import AntennaSchema
from ...admin.clients.referents.schema import (
    ReferentSchema,
    ReferentCreateMissionSchema,
)
from ...admin.clients.schema import ClientSchema
from ...common.schemas import PaginatedSchema, DocumentSchema
from ...thematique.schema import ThematiqueMissionSchema


class MissionSchema(SQLAlchemyAutoSchema):
    agency = fields.Nested(AgencySchema())
    antenna = fields.Nested(AntennaSchema())
    client = fields.Nested(ClientSchema())
    referents = fields.List(fields.Nested(ReferentSchema()))
    code_name = fields.String(dump_only=True)
    thematiques = fields.Nested(
        ThematiqueMissionSchema(), many=True, allow_none=True, required=False
    )

    class Meta:
        model = Mission
        include_fk = True
        unknown = EXCLUDE


class MissionLightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mission
        include_fk = False
        unknown = EXCLUDE


class MissionCreateSchema(SQLAlchemyAutoSchema):
    agency = fields.Nested(AgencySchema())
    antenna = fields.Nested(AntennaSchema())
    client = fields.Nested(ClientSchema())
    referents = fields.List(fields.Nested(ReferentCreateMissionSchema()))
    code_name = fields.String(dump_only=True)

    class Meta:
        model = Mission
        include_fk = True
        unknown = EXCLUDE


class MissionPaginatedSchema(PaginatedSchema):
    items = fields.Nested(MissionSchema(), many=True, dump_only=True)


class MissionDocumentSchema(DocumentSchema):
    pass
