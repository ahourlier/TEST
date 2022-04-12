from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, EXCLUDE
from app.project.simulations.model import (
    SimulationUseCase,
    SimulationAccommodation,
    SimulationSubResult,
    Simulation,
)
from app.common.schemas import PaginatedSchema
from app.funder.funders import FunderSchema
from app.funder.funders.schema import FunderLightSchema
from app.funder.funding_scenarios import FundingScenarioSchema
from app.project.accommodations.schema import (
    AccommodationSchema,
    AccommodationLightSchema,
)
from app.project.quotes.model import Quote
from app.project.quotes.model import QuoteWorkType


# SIMULATIONS_USE_CASES_SCHEMAS


class FunderDepositSchema(Schema):
    funder = fields.Nested(FunderLightSchema)
    deposit_date = fields.Date(allow_none=True)

    class Meta:
        unknown = EXCLUDE


class FunderPaymentRequestSchema(Schema):
    funder = fields.Nested(FunderLightSchema)
    payment_request_date = fields.Date(allow_none=True)

    class Meta:
        unknown = EXCLUDE


class FunderCertifiedSchema(Schema):
    funder = fields.Nested(FunderLightSchema)
    certification_date = fields.Date(allow_none=True)

    class Meta:
        unknown = EXCLUDE


class SimulationUseCaseSchema(SQLAlchemyAutoSchema):
    simulation_id = fields.Integer(required=False)

    class Meta:
        model = SimulationUseCase


# QUOTES SCHEMAS


class QuoteWorkTypeSchema(SQLAlchemyAutoSchema):
    quote_id = fields.Integer(required=False)

    class Meta:
        model = QuoteWorkType


class QuoteAccommodationSchema(Schema):

    quote_accommodation_id = fields.Integer(required=False)
    price_excl_tax = fields.Float(required=False)
    price_incl_tax = fields.Float(required=False)
    eligible_amount = fields.Float(required=False)
    accommodation = fields.Nested(AccommodationSchema())


class QuoteAccommodationLightSchema(Schema):

    quote_accommodation_id = fields.Integer(required=False)
    price_excl_tax = fields.Float(required=False)
    price_incl_tax = fields.Float(required=False)
    eligible_amount = fields.Float(required=False)
    accommodation = fields.Nested(AccommodationLightSchema(), required=False)

    class Meta:
        unknown = EXCLUDE


class SimulationLightSchema(SQLAlchemyAutoSchema):
    use_cases = fields.List(fields.Nested(SimulationUseCaseSchema()))
    funders = fields.List(fields.Nested(FunderSchema()), required=False)

    class Meta:
        model = Simulation
        include_fk = True


class QuoteSchema(SQLAlchemyAutoSchema):

    work_types = fields.List(fields.Nested(QuoteWorkTypeSchema()))
    is_used = fields.Boolean(dump_only=True)
    is_frozen = fields.Boolean(dump_only=True)
    simulations = fields.List(fields.Nested(SimulationLightSchema()), dump_only=True)
    accommodations = fields.List(
        fields.Nested(QuoteAccommodationSchema()), required=False
    )

    class Meta:
        model = Quote
        include_fk = True
        unknown = EXCLUDE


class QuoteLightSchema(SQLAlchemyAutoSchema):

    work_types = fields.List(fields.Nested(QuoteWorkTypeSchema()))
    is_used = fields.Boolean(dump_only=True)
    is_frozen = fields.Boolean(dump_only=True)
    accommodations = fields.List(
        fields.Nested(QuoteAccommodationLightSchema()), required=False
    )

    class Meta:
        model = Quote
        include_fk = True
        unknown = EXCLUDE


class QuotePaginatedSchema(PaginatedSchema):
    items = fields.Nested(QuoteSchema, many=True, dump_only=True)


# SIMULATIONS SUBRESULTS SCHEMA


class SimulationSubResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SimulationSubResult
        exclude = ["updated_at", "created_at"]
        unknown = EXCLUDE
        include_fk = True


# SIMULATIONS ACCOMMODATIONS SCHEMA


class SimulationAccommodationSchema(SQLAlchemyAutoSchema):
    accommodation = fields.Nested(AccommodationLightSchema)
    scenario_id = fields.Integer(
        required=False, allow_none=True
    )  # For PB requester, can select scenario for each accommodation

    class Meta:
        model = SimulationAccommodation
        exclude = ["updated_at", "created_at"]
        unknown = EXCLUDE


class SimulationAccommodationLightSchema(SQLAlchemyAutoSchema):
    accommodation = fields.Nested(AccommodationLightSchema)

    class Meta:
        model = SimulationAccommodation
        exclude = ["updated_at", "created_at", "rent_per_msq", "rent_type", "rent"]
        unknown = EXCLUDE


# FUNDER ACCOMMODATION SCHEMA


class FunderAccommodationSchema(Schema):
    id = fields.Integer(required=False, allow_none=True)
    accommodation = fields.Nested(
        AccommodationLightSchema, required=False, allow_none=True
    )
    rate = fields.Integer(required=False, allow_none=True)
    subventioned_expense = fields.Float(required=False, allow_none=True)
    is_common_area = fields.Boolean(required=False)
    scenario = fields.Nested(FundingScenarioSchema, allow_none=True)
    common_area_surface = fields.Float(allow_none=True, required=False, dump_only=True)
    eligible_cost = fields.Float(allow_none=True, load_only=True)
    upper_limit = fields.Float(allow_none=True, load_only=True)
    subvention = fields.Float(allow_none=True, load_only=True)

    class Meta:
        unknown = EXCLUDE


# SIMULATIONS SCHEMAS


class SimulationFunderSchema(Schema):
    funder = fields.Nested(FunderSchema)
    rate = fields.Integer(required=False, allow_none=True)
    advance = fields.Float(required=False, allow_none=True)
    subventioned_expense = fields.Float(required=False, allow_none=True)
    scenario = fields.Nested(FundingScenarioSchema, allow_none=True)
    reset_scenario = fields.Boolean(required=False, allow_none=True)
    funder_accommodations = fields.List(
        fields.Nested(FunderAccommodationSchema()), required=False
    )
    simulation_funder_id = fields.Integer()
    base_funder_id = fields.Integer(dump_only=True)
    eligible_cost = fields.Float(allow_none=True, load_only=True)
    upper_limit = fields.Float(allow_none=True, load_only=True)
    subvention = fields.Float(allow_none=True, load_only=True)

    class Meta:
        unknown = EXCLUDE


class SimulationSchema(SQLAlchemyAutoSchema):
    project_id = fields.Integer(required=True)
    use_cases = fields.List(fields.Nested(SimulationUseCaseSchema()))
    quotes = fields.List(fields.Nested(QuoteLightSchema()), required=False)
    funders = fields.List(fields.Nested(SimulationFunderSchema))
    deposit_funders = fields.List(fields.Nested(FunderDepositSchema()), dump_only=True)
    payment_request_funders = fields.List(
        fields.Nested(FunderPaymentRequestSchema()), dump_only=True
    )
    certification_funders = fields.List(
        fields.Nested(FunderCertifiedSchema()), dump_only=True
    )
    simulations_accommodations = fields.List(
        fields.Nested(SimulationAccommodationSchema)
    )
    quotes_modified = fields.Boolean(dump_only=True)
    sub_results = fields.List(
        fields.Nested(SimulationSubResultSchema()), required=False
    )
    scenario_id = fields.Integer(required=False, allow_none=True)

    class Meta:
        model = Simulation
        include_fk = True
        unknown = EXCLUDE
        load_only = [
            "total_work_price",
            "total_subventions",
            "remaining_costs",
            "subvention_on_TTC",
            "total_advances",
        ]


class SimulationPaginatedSchema(PaginatedSchema):
    items = fields.Nested(SimulationSchema, many=True, dump_only=True)


class HelperReinitializedSimulationsFundersSchema(Schema):
    project_id = fields.Integer(required=True)
    funders_id = fields.List(fields.Integer, required=True)
    accommodations_id = fields.List(fields.Integer, required=False)
    quotes_id = fields.List(fields.Integer, required=False)


class SimulationQuotesId(Schema):
    quotes_id = fields.List(fields.Integer, required=True)


class SimulationFundersId(Schema):
    funders_id = fields.List(fields.Integer, required=True)
