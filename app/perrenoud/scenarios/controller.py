from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_restx import inputs
from flask_sqlalchemy import Pagination

from . import api, Scenario
from .schema import ScenarioSchema
from .interface import ScenarioInterface
from .schema import ScenarioPaginatedSchema
from .service import (
    ScenarioService,
    SCENARIOS_DEFAULT_PAGE,
    SCENARIOS_DEFAULT_PAGE_SIZE,
    SCENARIOS_DEFAULT_SORT_FIELD,
    SCENARIOS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class ScenarioResource(AuthenticatedApi):
    """Scenarios"""

    @accepts(schema=ScenarioSchema, api=api)
    @responds(schema=ScenarioSchema)
    def post(self) -> Scenario:
        """Create an scenario"""
        return ScenarioService.create(request.parsed_obj)


@api.route("/accommodation/<int:accommodation_id>")
class ScenarioByAccommodationResource(AuthenticatedApi):
    """Scenarios by accommodation"""

    @accepts(
        *SEARCH_PARAMS,
        dict(name="include_initial_state", type=inputs.boolean),
        api=api,
    )
    @responds(schema=ScenarioPaginatedSchema())
    def get(self, accommodation_id: int) -> Pagination:
        """Get all scenarios by accommodation"""
        return ScenarioService.get_all(
            accommodation_id,
            page=int(request.args.get("page", SCENARIOS_DEFAULT_PAGE)),
            size=int(request.args.get("size", SCENARIOS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", SCENARIOS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", SCENARIOS_DEFAULT_SORT_DIRECTION
            ),
            include_initial_state=True
            if request.args.get("include_initial_state") == "True"
            else False,
        )


@api.route("/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class ScenarioIdResource(AuthenticatedApi):
    @responds(schema=ScenarioSchema)
    def get(self, scenario_id: int) -> Scenario:
        """Get single scenario"""

        return ScenarioService.get_by_id(scenario_id)

    def delete(self, scenario_id: int) -> Response:
        """Delete single scenario"""

        id = ScenarioService.delete_by_id(scenario_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(dict(name="section", type=str), schema=ScenarioSchema, api=api)
    @responds(schema=ScenarioSchema)
    def put(
        self,
        scenario_id: int,
    ) -> Scenario:
        """Update single scenario"""

        changes: ScenarioInterface = request.parsed_obj
        db_scenario = ScenarioService.get_by_id(scenario_id)
        return ScenarioService.update(
            db_scenario,
            changes,
            section=str(request.args.get("section"))
            if request.args.get("section") not in [None, ""]
            else None,
        )


@api.route("/initial_state/<int:accommodation_id>")
@api.param("accommodationId", "Accommodation unique ID")
class ScenarioByAccommodationIdResource(AuthenticatedApi):
    @responds(schema=ScenarioSchema)
    def get(self, accommodation_id: int) -> Scenario:
        """Get single scenario"""

        return ScenarioService.get_initial_state_by_accommodation_id(accommodation_id)


@api.route("/clone/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class ScenarioDuplicationResource(AuthenticatedApi):
    @responds(schema=ScenarioSchema)
    def put(
        self,
        scenario_id: int,
    ) -> Scenario:
        """Duplicate a scenario and return the clone"""
        return ScenarioService.duplicate(scenario_id)


@api.route("/<int:scenario_id>/analysis")
@api.param("scenarioId", "Scenario unique ID")
class LaunchAnalysisResource(AuthenticatedApi):
    @responds(schema=ScenarioSchema)
    def get(self, scenario_id: int) -> Scenario:
        """Update analysis values for one scenario"""
        return ScenarioService.launch_perrenoud_analysis(
            scenario_id,
        )


@api.route("/<int:scenario_id>/analysis_test")
@api.param("scenarioId", "Scenario unique ID")
class TestXMLResource(AuthenticatedApi):
    def get(self, scenario_id: int) -> Scenario:
        """Get xml perrenoud generated for a single scenario"""
        return ScenarioService.launch_perrenoud_analysis(scenario_id, test_XML=True)


@api.route("/clone_initial_state/<int:accommodation_id>")
@api.param("accommodationId", "Accommodation unique ID")
class InitialStateCreationAndDuplicationResource(AuthenticatedApi):
    @responds(schema=ScenarioSchema)
    def put(
        self,
        accommodation_id: int,
    ) -> Scenario:
        """Create a scenario and return the clone"""
        return ScenarioService.create_and_duplicate(accommodation_id)
