from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.combined_structure.model import CombinedStructure
from app.common.address.schema import AddressSchema
from app.common.schemas import PaginatedSchema

from app.copro.president.schema import PresidentSchema, PresidentCreateSchema
from app.copro.syndic.schema import SyndicSchema, SyndicCreateSchema



class CombinedStructureCreateSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentCreateSchema())
    syndics = fields.List(fields.Nested(SyndicCreateSchema()))

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructureUpdateSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentCreateSchema(), dump_only=True)
    # syndics = fields.List(fields.Nested(SyndicSchema()), dump_only=True)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructureSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema())
    syndics = fields.List(fields.Nested(SyndicSchema()), dump_only=True)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructurePaginatedSchema(PaginatedSchema):
    items = fields.Nested(CombinedStructureSchema(), many=True, dump_only=True)

