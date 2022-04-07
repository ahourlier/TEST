from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.building.schema import BuildingForLotSchema
from app.cle_repartition.schema import (
    LotCleRepartitionSchema,
    LotCleRepartitionCreateSchema,
)
from app.person.schema import PersonSchema
from app.common.schemas import PaginatedSchema
from app.copro.copros.schema import CoproForLotsSchema
from app.lot import Lot


class LotCreateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=True, allow_none=False)
    building_id = fields.Integer(required=True, allow_none=False)
    owners = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    occupants = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(fields.Nested(LotCleRepartitionCreateSchema()))

    class Meta:
        model = Lot
        include_fk = True


class LotUpdateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=False)
    building_id = fields.Integer(required=False)
    owners = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    occupants = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(fields.Nested(LotCleRepartitionCreateSchema()))

    class Meta:
        model = Lot
        include_fk = True


class LotSchema(SQLAlchemyAutoSchema):
    owners = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    occupants = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(
        fields.Nested(LotCleRepartitionSchema()), dump_only=True
    )

    class Meta:
        model = Lot
        include_fk = True


class LotListSchema(SQLAlchemyAutoSchema):
    copro = fields.Nested(CoproForLotsSchema(), dump_only=True)
    building = fields.Nested(BuildingForLotSchema(), dump_only=True)
    owners = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(
        fields.Nested(LotCleRepartitionSchema()), dump_only=True
    )

    class Meta:
        model = Lot
        include_fk = True


class LotPaginatedSchema(PaginatedSchema):
    items = fields.Nested(LotListSchema(), many=True, dump_only=True)
