from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, Schema

from app.funder.funding_scenarios.model import FundingScenario


class FundingScenarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FundingScenario
        include_fk = True


class FundingScenarioListSchema(Schema):
    items = fields.Nested(FundingScenarioSchema, many=True, dump_only=True)
