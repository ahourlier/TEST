from flask import request
from flask_accepts import accepts, responds

from . import api
from .service import (
    SimulationDepositService,
    SimulationPaymentRequestService,
    SimulationCertifiedService,
)
from ..simulations import SimulationSchema, Simulation
from ..simulations.interface import SimulationInterface
from ..simulations.schema import (
    SimulationFundersId,
    FunderDepositSchema,
    FunderPaymentRequestSchema,
    FunderCertifiedSchema,
)
from ...common.api import AuthenticatedApi


@api.route("/<int:simulation_id>/deposit/edit_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationDepositEditResource(AuthenticatedApi):
    @accepts(schema=FunderDepositSchema(many=True), api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Add funder(s) to a simulation, as deposit"""
        deposit_funders_list = request.parsed_obj
        return SimulationDepositService.edit_funders_list(
            deposit_funders_list, simulation_id
        )


@api.route("/<int:simulation_id>/deposit/remove_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationDepositRemoveResource(AuthenticatedApi):
    @accepts(schema=SimulationFundersId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Remove funder(s) from a simulation"""
        funders_id = request.parsed_obj
        return SimulationDepositService.delete_by_funders_id(funders_id, simulation_id)


@api.route("/<int:simulation_id>/payment/edit_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationPaymentEditResource(AuthenticatedApi):
    @accepts(schema=FunderPaymentRequestSchema(many=True), api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Add funder(s) to a simulation, as payment request"""
        payment_funders_list = request.parsed_obj
        return SimulationPaymentRequestService.edit_funders_list(
            payment_funders_list, simulation_id
        )


@api.route("/<int:simulation_id>/payment/remove_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationPaymentRemoveResource(AuthenticatedApi):
    @accepts(schema=SimulationFundersId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Remove funder(s) from a simulation"""
        funders_id = request.parsed_obj
        return SimulationPaymentRequestService.delete_by_funders_id(
            funders_id, simulation_id
        )


@api.route("/<int:simulation_id>/certification/edit_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationCertificationEditResource(AuthenticatedApi):
    @accepts(schema=FunderCertifiedSchema(many=True), api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Add funder(s) to a simulation, as certification"""
        certification_funders_list = request.parsed_obj
        return SimulationCertifiedService.edit_funders_list(
            certification_funders_list, simulation_id
        )


@api.route("/<int:simulation_id>/certification/remove_funders")
@api.param("simulationId", "Simulation unique ID")
class SimulationCertificationRemoveResource(AuthenticatedApi):
    @accepts(schema=SimulationFundersId, api=api)
    @responds(schema=SimulationSchema)
    def put(self, simulation_id: int) -> Simulation:
        """Remove funder(s) from a simulation"""
        funders_id = request.parsed_obj
        return SimulationCertifiedService.delete_by_funders_id(
            funders_id, simulation_id
        )
