from . import api, SimulationSchema, Simulation

from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from .interface import SimulationInterface, SimulationFunderInterface
from .schema import (
    SimulationPaginatedSchema,
    SimulationQuotesId,
    SimulationFundersId,
    SimulationFunderSchema,
    HelperReinitializedSimulationsFundersSchema,
)
from .service import (
    SimulationService,
    SIMULATIONS_DEFAULT_PAGE,
    SIMULATIONS_DEFAULT_PAGE_SIZE,
    SIMULATIONS_DEFAULT_SORT_FIELD,
    SIMULATIONS_DEFAULT_SORT_DIRECTION,
    SimulationQuoteService,
    SimulationFunderService,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS
from ...funder.funders import FunderSchema


@api.route("/")
class SimulationResource(AuthenticatedApi):
    """ Simulations """

    @accepts(
        *SEARCH_PARAMS,
        dict(name="quote_id", type=int),
        dict(name="funder_id", type=int),
        dict(name="project_id", type=int),
        dict(name="use_case", type=str),
        api=api,
    )
    @responds(schema=SimulationPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all simulations """
        return SimulationService.get_all(
            page=int(request.args.get("page", SIMULATIONS_DEFAULT_PAGE)),
            size=int(request.args.get("size", SIMULATIONS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", SIMULATIONS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", SIMULATIONS_DEFAULT_SORT_DIRECTION
            ),
            quote_id=int(request.args.get("quote_id"))
            if request.args.get("quote_id") not in [None, ""]
            else None,
            funder_id=int(request.args.get("funder_id"))
            if request.args.get("funder_id") not in [None, ""]
            else None,
            project_id=int(request.args.get("project_id"))
            if request.args.get("project_id") not in [None, ""]
            else None,
            use_case=str(request.args.get("use_case"))
            if request.args.get("use_case") not in [None, ""]
            else None,
        )

    @accepts(schema=SimulationSchema, api=api)
    @responds(schema=SimulationSchema)
    def post(self) -> Simulation:
        """ Create a simulation """
        return SimulationService.create(request.parsed_obj)


@api.route("/<int:simulation_id>")
@api.param("simulationId", "Simulation unique ID")
class SimulationIdResource(AuthenticatedApi):
    @responds(schema=SimulationSchema)
    def get(self, simulation_id: int) -> Simulation:
        """ Get single simulation """

        return SimulationService.get_by_id(simulation_id)

    def delete(self, simulation_id: int) -> Response:
        """Delete single simulation"""

        id = SimulationService.delete_by_id(simulation_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=SimulationSchema, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Update single simulation"""
        changes: SimulationInterface = request.parsed_obj
        db_simulation = SimulationService.get_by_id(simulation_id)
        return SimulationService.update(db_simulation, changes)


@api.route("/<int:simulation_id>/add_quotes")
@api.param("simulationId", "Simulation unique ID")
class SimulationQuotesAddResource(AuthenticatedApi):
    @accepts(schema=SimulationQuotesId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Add quote(s) to a simulation"""

        quotes_id: SimulationInterface = request.parsed_obj
        return SimulationQuoteService.create_by_quotes_id(quotes_id, simulation_id)


@api.route("/<int:simulation_id>/add_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationFundersAddResource(AuthenticatedApi):
    @accepts(schema=SimulationFundersId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Add funder(s) to a simulation"""

        funders_id: SimulationInterface = request.parsed_obj
        return SimulationFunderService.create_by_funders_id(funders_id, simulation_id)


@api.route("/<int:simulation_id>/remove_quotes")
@api.param("simulationId", "Simulation unique ID")
class SimulationQuotesRemoveResource(AuthenticatedApi):
    @accepts(schema=SimulationQuotesId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Remove quote(s) to a simulation"""

        quotes_id: SimulationInterface = request.parsed_obj
        return SimulationQuoteService.delete_by_quotes_id(quotes_id, simulation_id)


@api.route("/<int:simulation_id>/remove_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationFundersRemoveResource(AuthenticatedApi):
    @accepts(schema=SimulationFundersId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Remove funder(s) to a simulation"""

        funders_id: SimulationInterface = request.parsed_obj
        return SimulationFunderService.delete_by_funders_id(funders_id, simulation_id)


@api.route("/<int:simulation_id>/clone")
@api.param("simulationId", "Simulation unique ID")
class SimulationDuplicateResource(AuthenticatedApi):
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Duplicate a simulation"""

        return SimulationService.duplicate(simulation_id)


@api.route("/funder/reset")
class HelperResetScenarioFunderResource(AuthenticatedApi):
    # TODO Obsolete Endpoint. To remove when sure it's not usefull
    # @accepts(
    #     *SEARCH_PARAMS,
    #     dict(name="funder_id", type=int),
    #     dict(name="project_id", type=int),
    #     api=api,
    # )
    # @responds(schema=SimulationFunderSchema(many=True))
    # def get(self) -> Simulation:
    #     """ Get informations about original funder and match scenario """
    #     return SimulationFunderService.get_reinitialized_simulations_funders(
    #         funders_id=int(request.args.get("funder_id"))
    #         if request.args.get("funder_id") not in [None, ""]
    #         else None,
    #         project_id=int(request.args.get("project_id"))
    #         if request.args.get("project_id") not in [None, ""]
    #         else None,
    #     )

    @accepts(
        *SEARCH_PARAMS,
        dict(name="requester_type", type=str),
        schema=HelperReinitializedSimulationsFundersSchema,
        api=api,
    )
    @responds(schema=SimulationFunderSchema(many=True))
    def post(self) -> Simulation:
        """ Get informations about multiples funders and match scenario """

        payload: SimulationInterface = request.parsed_obj

        accommodations_id = (
            payload["accommodations_id"] if "accommodations_id" in payload else None
        )
        quotes_id = payload["quotes_id"] if "quotes_id" in payload else None
        return SimulationFunderService.get_reinitialized_simulations_funders(
            project_id=payload["project_id"],
            funders_id=payload["funders_id"],
            accommodations_id=accommodations_id,
            quotes_id=quotes_id,
            requester_type=str(request.args.get("requester_type"))
            if request.args.get("requester_type") not in [None, ""]
            else None,
        )
