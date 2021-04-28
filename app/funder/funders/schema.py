from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE, Schema

from app.funder.funders.model import Funder
from app.common.schemas import PaginatedSchema
from app.funder.funding_scenarios import FundingScenarioSchema


class FunderSchema(SQLAlchemyAutoSchema):
    is_national = fields.Boolean(dump_only=True)
    is_duplicate = fields.Boolean(dump_only=True)
    funding_scenarios = fields.Nested(FundingScenarioSchema, many=True)

    class Meta:
        model = Funder
        include_fk = True
        unknown = EXCLUDE


class FunderLightSchema(SQLAlchemyAutoSchema):
    is_national = fields.Boolean(dump_only=True)

    class Meta:
        model = Funder
        include_fk = True
        unknown = EXCLUDE


class FunderWithScenarioSchema(Schema):
    funder = fields.Nested(FunderLightSchema, dump_only=True)
    scenario = fields.Nested(FundingScenarioSchema, dump_only=True)
    rate = fields.Integer(dump_only=True)
    advance = fields.Integer(dump_only=True)
    subventioned_expense = fields.Integer(dump_only=True)
    simulation_funder_id = fields.Integer(dump_only=True)

    class Meta:
        unknown: EXCLUDE


class FunderPaginatedSchema(PaginatedSchema):
    items = fields.Nested(FunderSchema, many=True, dump_only=True)


class FunderDuplicateSchema(Schema):
    mission_id = fields.Integer(required=True)
    funders_id = fields.List(fields.Integer(), required=False)
