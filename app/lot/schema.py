from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.building.schema import BuildingForLotSchema
from app.cle_repartition.schema import LotCleRepartitionSchema
from app.person.schema import PersonSchema
from app.common.schemas import PaginatedSchema
from app.copro.copros.schema import CoproForLotsSchema
from app.lot import Lot


class LotCreateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=True, allow_none=False)
    occupants = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(fields.Nested(LotCleRepartitionSchema()))

    class Meta:
        model = Lot
        include_fk = True


class LotUpdateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=False)
    occupants = fields.List(fields.Nested(PersonSchema()), allow_none=True)
    cles_repartition = fields.List(fields.Nested(LotCleRepartitionSchema()))

    class Meta:
        model = Lot
        include_fk = True


class LotSchema(SQLAlchemyAutoSchema):
    owner = fields.Nested(PersonSchema(), dump_only=True)
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
    owner = fields.Nested(PersonSchema(), dump_only=True)
    cles_repartition = fields.List(
        fields.Nested(LotCleRepartitionSchema()), dump_only=True
    )

    class Meta:
        model = Lot
        include_fk = True


class LotPaginatedSchema(PaginatedSchema):
    items = fields.Nested(LotListSchema(), many=True, dump_only=True)
