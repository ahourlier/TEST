from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.combined_structure.model import CombinedStructure
from app.combined_structure.service import CombinedStructureService
from app.common.schemas import PaginatedSchema

from app.copro.president.schema import PresidentSchema, PresidentCreateSchema
from app.copro.syndic.schema import SyndicSchema, SyndicCreateSchema


class CombinedStructureCreateSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentCreateSchema())
    president_id = fields.Integer(allow_none=True, required=False)
    syndics = fields.List(fields.Nested(SyndicCreateSchema()))
    account_closing_date = fields.String(allow_none=True, required=False)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructureUpdateSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentCreateSchema())
    account_closing_date = fields.String(allow_none=True, required=False)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructureSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema())
    syndics = fields.List(fields.Nested(SyndicSchema()), dump_only=True)
    tantiemes = fields.Method("get_tantiemes_for_cs")

    def get_tantiemes_for_cs(self, obj):
        return CombinedStructureService.get_tantiemes_for_cs(obj)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructureForListSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema())
    syndics = fields.List(fields.Nested(SyndicSchema()), dump_only=True)

    class Meta:
        model = CombinedStructure
        include_fk = True


class CombinedStructurePaginatedSchema(PaginatedSchema):
    items = fields.Nested(CombinedStructureForListSchema(), many=True, dump_only=True)
