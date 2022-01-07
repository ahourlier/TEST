from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from app.cle_repartition.model import CleRepartition, LotCleRepartition


class CleRepartitionSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = CleRepartition


class CleRepartitionCreateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=False)

    class Meta:
        model = CleRepartition


class LotCleRepartitionSchema(SQLAlchemyAutoSchema):
    cle_repartition = fields.Nested(CleRepartitionSchema(), dump_only=True)

    class Meta:
        model = LotCleRepartition


class LotCleRepartitionCreateSchema(SQLAlchemyAutoSchema):
    lot_id = fields.Integer(required=False)

    class Meta:
        model = LotCleRepartition
