from app import db
from app.project.comments.service import (
    DEPOSIT_DATE_UPDATE,
    PAYMENT_DATE_UPDATE,
    CERTIFICATION_DATE_UPDATE,
)
from app.project.simulations import Simulation
from app.project.simulations.model import (
    SimulationDeposit,
    SimulationPaymentRequest,
    SimulationCertified,
)

import app.project.simulations.service as simulations_service
import app.project.comments.service as comments_service
from app.project.simulations_uses.exceptions import (
    SimulationDepositNotFoundException,
    SimulationPaymentRequestNotFoundException,
    SimulationCertifiedNotFoundException,
)
from app.project.simulations_uses.interface import (
    SimulationDepositInterface,
    SimulationPaymentRequestInterface,
    SimulationCertifiedInterface,
)


class SimulationDepositService:
    @staticmethod
    def create(simulation_id: str, new_funder: dict) -> SimulationDeposit:
        # Check than entity does exist
        simulations_service.SimulationService.get_by_id(simulation_id)
        new_attrs = {
            "simulation_id": simulation_id,
            "funder_id": new_funder["funder"]["id"],
            "deposit_date": new_funder["deposit_date"],
        }
        simulation_deposit = SimulationDeposit(
            **SimulationDepositInterface(**new_attrs)
        )
        db.session.add(simulation_deposit)
        db.session.commit()

        if simulation_deposit.deposit_date is not None:
            comments_service.AutomaticCommentService.automatic_funder_comment(
                DEPOSIT_DATE_UPDATE,
                simulation_deposit.funder.name,
                simulation_deposit.simulation.project,
            )

        return simulation_deposit

    @staticmethod
    def create_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for new_funder_id in funders_id["funders_id"]:
            SimulationDepositService.create(simulation_id, new_funder_id)
        return simulation

    @staticmethod
    def edit_funders_list(funders_list, simulation_id):
        """
        - Create new simulation_deposit relation if they don't exist yet
        - Update existing simulation_deposit (i.e. update "deposit_date" field)
        """
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        existing_deposit_funders_id = [
            deposit_funder.funder_id for deposit_funder in simulation.deposit_funders
        ]
        for deposit_funder in funders_list:
            if deposit_funder["funder"]["id"] in existing_deposit_funders_id:
                SimulationDepositService.update(simulation, deposit_funder)
            else:
                SimulationDepositService.create(simulation_id, deposit_funder)
        return simulation

    @staticmethod
    def get_by_id(simulation_deposit_id: str) -> SimulationDeposit:
        db_simulation = SimulationDeposit.query.get(simulation_deposit_id)
        if db_simulation is None:
            raise SimulationDepositNotFoundException
        return db_simulation

    @staticmethod
    def delete_by_id(simulation_deposit_id: int) -> int or None:
        # Check than entity does exist
        simulation_deposit = SimulationDepositService.get_by_id(simulation_deposit_id)
        db.session.delete(simulation_deposit)
        db.session.commit()
        return simulation_deposit_id

    @staticmethod
    def delete_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for removed_funder_id in funders_id["funders_id"]:
            for deposit_funder in simulation.deposit_funders:
                if removed_funder_id == deposit_funder.funder_id:
                    SimulationDepositService.delete_by_id(deposit_funder.id)
        return simulation

    @staticmethod
    def delete_all(simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for deposit_funder in simulation.deposit_funders:
            SimulationDepositService.delete_by_id(deposit_funder.id)
        return simulation

    @staticmethod
    def update(
        simulation: Simulation, changes: dict, force_update: bool = False
    ) -> SimulationDeposit:
        simulation_deposit = (
            SimulationDeposit.query.filter(
                SimulationDeposit.simulation_id == simulation.id
            )
            .filter(SimulationDeposit.funder_id == changes["funder"]["id"])
            .first()
        )
        del changes["funder"]  # Updating funder is not necessary
        if force_update or SimulationDepositService.has_changed(
            simulation_deposit, changes
        ):
            if (
                "deposit_date" in changes
                and changes["deposit_date"] is not simulation_deposit.deposit_date
            ):
                comments_service.AutomaticCommentService.automatic_funder_comment(
                    DEPOSIT_DATE_UPDATE,
                    simulation_deposit.funder.name,
                    simulation_deposit.simulation.project,
                )
            simulation_deposit.update(changes)
            db.session.commit()
        return simulation_deposit

    @staticmethod
    def has_changed(
        simulation_deposit: SimulationDeposit, changes: SimulationDepositInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(simulation_deposit, key) != value:
                return True
        return False


class SimulationPaymentRequestService:
    @staticmethod
    def create(simulation_id: str, new_funder: dict) -> SimulationPaymentRequest:
        # Check than entity does exist
        simulations_service.SimulationService.get_by_id(simulation_id)
        new_attrs = {
            "simulation_id": simulation_id,
            "funder_id": new_funder["funder"]["id"],
            "payment_request_date": new_funder["payment_request_date"],
        }
        simulation_payment_request = SimulationPaymentRequest(
            **SimulationPaymentRequestInterface(**new_attrs)
        )
        db.session.add(simulation_payment_request)
        db.session.commit()

        if simulation_payment_request.payment_request_date is not None:
            comments_service.AutomaticCommentService.automatic_funder_comment(
                PAYMENT_DATE_UPDATE,
                simulation_payment_request.funder.name,
                simulation_payment_request.simulation.project,
            )

        return simulation_payment_request

    @staticmethod
    def create_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for new_funder_id in funders_id["funders_id"]:
            SimulationPaymentRequestService.create(simulation_id, new_funder_id)
        return simulation

    @staticmethod
    def edit_funders_list(funders_list, simulation_id):
        """
        - Create new simulation_payment_request relation if they don't exist yet
        - Update existing simulation_payment_request (i.e. update "payment_request_date" field)
        """
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        existing_payment_request_funders_id = [
            payment_request_funder.funder_id
            for payment_request_funder in simulation.payment_request_funders
        ]
        for payment_request_funder in funders_list:
            if (
                payment_request_funder["funder"]["id"]
                in existing_payment_request_funders_id
            ):
                SimulationPaymentRequestService.update(
                    simulation, payment_request_funder
                )
            else:
                SimulationPaymentRequestService.create(
                    simulation_id, payment_request_funder
                )
        return simulation

    @staticmethod
    def get_by_id(simulation_payment_request_id: str) -> SimulationPaymentRequest:
        db_simulation = SimulationPaymentRequest.query.get(
            simulation_payment_request_id
        )
        if db_simulation is None:
            raise SimulationPaymentRequestNotFoundException
        return db_simulation

    @staticmethod
    def delete_by_id(simulation_payment_request_id: int) -> int or None:
        # Check than entity does exist
        simulation_payment_request = SimulationPaymentRequestService.get_by_id(
            simulation_payment_request_id
        )
        db.session.delete(simulation_payment_request)
        db.session.commit()
        return simulation_payment_request_id

    @staticmethod
    def delete_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for removed_funder_id in funders_id["funders_id"]:
            for payment_request_funder in simulation.payment_request_funders:
                if removed_funder_id == payment_request_funder.funder_id:
                    SimulationPaymentRequestService.delete_by_id(
                        payment_request_funder.id
                    )
        return simulation

    @staticmethod
    def delete_all(simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for payment_request_funder in simulation.payment_request_funders:
            SimulationPaymentRequestService.delete_by_id(payment_request_funder.id)
        return simulation

    @staticmethod
    def update(
        simulation: Simulation, changes: dict, force_update: bool = False
    ) -> SimulationPaymentRequest:
        simulation_payment_request = (
            SimulationPaymentRequest.query.filter(
                SimulationPaymentRequest.simulation_id == simulation.id
            )
            .filter(SimulationPaymentRequest.funder_id == changes["funder"]["id"])
            .first()
        )
        del changes["funder"]  # Updating funder is not necessary here
        if force_update or SimulationPaymentRequestService.has_changed(
            simulation_payment_request, changes
        ):
            if (
                "payment_request_date" in changes
                and changes["payment_request_date"]
                is not simulation_payment_request.payment_request_date
            ):
                comments_service.AutomaticCommentService.automatic_funder_comment(
                    PAYMENT_DATE_UPDATE,
                    simulation_payment_request.funder.name,
                    simulation_payment_request.simulation.project,
                )
            simulation_payment_request.update(changes)
            db.session.commit()
        return simulation_payment_request

    @staticmethod
    def has_changed(
        simulation_payment_request: SimulationPaymentRequest,
        changes: SimulationPaymentRequestInterface,
    ) -> bool:
        for key, value in changes.items():
            if getattr(simulation_payment_request, key) != value:
                return True
        return False


class SimulationCertifiedService:
    @staticmethod
    def create(simulation_id: str, new_funder: dict) -> SimulationCertified:
        # Check than entity does exist
        simulations_service.SimulationService.get_by_id(simulation_id)
        new_attrs = {
            "simulation_id": simulation_id,
            "funder_id": new_funder["funder"]["id"],
            "certification_date": new_funder["certification_date"],
        }
        simulation_certified = SimulationCertified(
            **SimulationCertifiedInterface(**new_attrs)
        )
        db.session.add(simulation_certified)
        db.session.commit()

        if simulation_certified.certification_date is not None:
            comments_service.AutomaticCommentService.automatic_funder_comment(
                CERTIFICATION_DATE_UPDATE,
                simulation_certified.funder.name,
                simulation_certified.simulation.project,
            )

        return simulation_certified

    @staticmethod
    def create_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for new_funder_id in funders_id["funders_id"]:
            SimulationCertifiedService.create(simulation_id, new_funder_id)
        return simulation

    @staticmethod
    def edit_funders_list(funders_list, simulation_id):
        """
        - Create new simulation_certified relation if they don't exist yet
        - Update existing simulation_certified (i.e. update "certification_date" field)
        """
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        existing_certified_funders_id = [
            certified_funder.funder_id
            for certified_funder in simulation.certification_funders
        ]
        for certified_funder in funders_list:
            if certified_funder["funder"]["id"] in existing_certified_funders_id:
                SimulationCertifiedService.update(simulation, certified_funder)
            else:
                SimulationCertifiedService.create(simulation_id, certified_funder)
        return simulation

    @staticmethod
    def get_by_id(simulation_certified_id: str) -> SimulationCertified:
        db_simulation = SimulationCertified.query.get(simulation_certified_id)
        if db_simulation is None:
            raise SimulationCertifiedNotFoundException
        return db_simulation

    @staticmethod
    def delete_by_id(simulation_certified_id: int) -> int or None:
        # Check than entity does exist
        simulation_certified = SimulationCertifiedService.get_by_id(
            simulation_certified_id
        )
        db.session.delete(simulation_certified)
        db.session.commit()
        return simulation_certified_id

    @staticmethod
    def delete_by_funders_id(funders_id, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for removed_funder_id in funders_id["funders_id"]:
            for certification_funder in simulation.certification_funders:
                if removed_funder_id == certification_funder.funder_id:
                    SimulationCertifiedService.delete_by_id(certification_funder.id)
        return simulation

    @staticmethod
    def delete_all(simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        for certification_funder in simulation.certification_funders:
            SimulationCertifiedService.delete_by_id(certification_funder.id)
        return simulation

    @staticmethod
    def update(
        simulation: Simulation, changes: dict, force_update: bool = False
    ) -> SimulationCertified:
        simulation_certification = (
            SimulationCertified.query.filter(
                SimulationCertified.simulation_id == simulation.id
            )
            .filter(SimulationCertified.funder_id == changes["funder"]["id"])
            .first()
        )
        del changes["funder"]  # Updating funder is not necessary
        if force_update or SimulationCertifiedService.has_changed(
            simulation_certification, changes
        ):
            if (
                "certification_date" in changes
                and changes["certification_date"]
                is not simulation_certification.certification_date
            ):
                comments_service.AutomaticCommentService.automatic_funder_comment(
                    CERTIFICATION_DATE_UPDATE,
                    simulation_certification.funder.name,
                    simulation_certification.simulation.project,
                )
            simulation_certification.update(changes)
            db.session.commit()
        return simulation_certification

    @staticmethod
    def has_changed(
        simulation_deposit: SimulationCertified, changes: SimulationCertifiedInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(simulation_deposit, key) != value:
                return True
        return False
