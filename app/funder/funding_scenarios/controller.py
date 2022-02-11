from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires

from . import api
from .interface import FundingScenarioInterface
from .model import FundingScenario, FUNDING_SCENARIOS_CRITERIA_CONFIGURATION
from .schema import (
    FundingScenarioSchema,
    FundingScenarioListSchema,
)
from .service import FundingScenarioService
from app.common.api import AuthenticatedApi
from app.common.permissions import can_manage_funders
from ..funders.service import FunderService
from ...referential.enums import AppEnum


@api.route("/")
class FundingScenarioResource(AuthenticatedApi):
    @accepts(dict(name="format", type=str), dict(name="funder_id", type=int), api=api)
    def get(self) -> Response:
        """
        Get all funding scenarios
        Can be filtered on a specific funderId
        If format=table request param is provided, formats the output to math scenario list table format
        """
        scenarios = FundingScenarioService.get_all(
            funder_id=request.args.get("funder_id", None)
        )
        if request.args.get("format", None) == "table":
            headers = []
            additional_headers = []
            items = []
            for scenario in scenarios:
                scenario_dict = {"id": scenario.id, "criteria": {}}
                for criterion in scenario.criteria:
                    if criterion.get("field") not in headers:
                        headers.append(criterion.get("field"))
                    scenario_dict["criteria"][criterion.get("field")] = criterion.get(
                        "value"
                    )
                if scenario.rate is not None:
                    if "scenario.rate" not in additional_headers:
                        additional_headers.append("scenario.rate")
                    scenario_dict["criteria"]["scenario.rate"] = scenario.rate
                if scenario.upper_limit is not None:
                    if "scenario.upper_limit" not in additional_headers:
                        additional_headers.append("scenario.upper_limit")
                    scenario_dict["criteria"][
                        "scenario.upper_limit"
                    ] = scenario.upper_limit
                if scenario.advance is not None:
                    if "scenario.advance" not in additional_headers:
                        additional_headers.append("scenario.advance")
                    scenario_dict["criteria"]["scenario.advance"] = scenario.advance
                if scenario.upper_surface_limit is not None:
                    if "scenario.upper_surface_limit" not in additional_headers:
                        additional_headers.append("scenario.upper_surface_limit")
                    scenario_dict["criteria"][
                        "scenario.upper_surface_limit"
                    ] = scenario.upper_surface_limit
                if scenario.upper_price_surface_limit is not None:
                    if "scenario.upper_price_surface_limit" not in additional_headers:
                        additional_headers.append("scenario.upper_price_surface_limit")
                    scenario_dict["criteria"][
                        "scenario.upper_price_surface_limit"
                    ] = scenario.upper_price_surface_limit
                items.append(scenario_dict)
            return jsonify(
                dict(headers=sorted(headers) + additional_headers, items=items)
            )
        else:
            return FundingScenarioListSchema().dump(dict(items=scenarios))

    @accepts(schema=FundingScenarioSchema, api=api)
    @responds(schema=FundingScenarioSchema, api=api)
    @requires(can_manage_funders)
    def post(self) -> FundingScenario:
        """Create a funding scenario"""

        return FundingScenarioService.create(request.parsed_obj, commit=True)


@api.route("/<int:funding_scenario_id>")
@api.param("fundingScenarioId", "Funding scenario unique ID")
class FundingScenarioIdResource(AuthenticatedApi):
    @responds(schema=FundingScenarioSchema, api=api)
    def get(self, funding_scenario_id: int) -> FundingScenario:
        return FundingScenarioService.get_by_id(funding_scenario_id)

    @requires(can_manage_funders)
    def delete(self, funding_scenario_id: int) -> Response:
        """Delete a funding scenario"""
        id = FundingScenarioService.delete_by_id(funding_scenario_id, commit=True)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=FundingScenarioSchema, api=api)
    @responds(schema=FundingScenarioSchema, api=api)
    @requires(can_manage_funders)
    def put(self, funding_scenario_id: int) -> FundingScenario:
        """Update a single funding scenario"""

        changes: FundingScenarioInterface = request.parsed_obj
        db_funding_scenario = FundingScenarioService.get_by_id(funding_scenario_id)
        return FundingScenarioService.update(db_funding_scenario, changes, commit=True)


@api.route("/criteria")
class FundingScenarioAvailableCriteriasResource(AuthenticatedApi):
    """To retrieve data needed to create new criterias"""

    def get(self):
        items = []
        enums_kinds = [
            x["enumKind"]
            for x in FUNDING_SCENARIOS_CRITERIA_CONFIGURATION.values()
            if x.get("enumKind", None) is not None
        ]
        db_enums = (
            AppEnum.query.filter(AppEnum.kind.in_(enums_kinds))
            .order_by(AppEnum.kind, AppEnum.display_order)
            .all()
        )
        dict_enums = {}
        for db_enum in db_enums:
            dict_enums.setdefault(db_enum.kind, []).append(db_enum.name)

        for field, value in FUNDING_SCENARIOS_CRITERIA_CONFIGURATION.items():
            field_object = {
                "name": field,
                "type": value["type"],
                "operators": value["operators"],
            }
            if value["type"] == "enum":
                field_object["values"] = dict_enums.get(value["enumKind"], [])
            items.append(field_object)

        return jsonify(dict(items=items))
