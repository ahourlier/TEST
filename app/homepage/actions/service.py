from datetime import date, datetime
from enum import Enum

import dateutil.relativedelta
from flask import g
from flask_sqlalchemy import Pagination
from sqlalchemy import not_
from sqlalchemy.sql.elements import or_

import app.project.projects.service as projects_service
from app.common.exceptions import InvalidSearchFieldException
from app.common.search import sort_query
from app.mission.missions import Mission
from app.mission.monitors import Monitor
from app.mission.monitors.model import MonitorField
from app.project.funders_monitoring_values import FunderMonitoringValue
from app.project.projects import Project
from app.project.projects.model import ProjectStatus
import app.project.funders_monitoring_values.service as monitoring_values_service
from app.project.projects.service import (
    PROJECTS_DEFAULT_PAGE,
    PROJECTS_DEFAULT_PAGE_SIZE,
    PROJECTS_DEFAULT_SORT_FIELD,
    PROJECTS_DEFAULT_SORT_DIRECTION,
)


class RequiredActionsService:
    @staticmethod
    def get_counts():
        return {
            "count_meet_advices_to_plan": RequiredActionsService.get_meet_advices_to_plan_alert().count(),
            "count_meet_to_process": RequiredActionsService.get_meet_to_process_alert().count(),
            "count_contact_to_call_again": RequiredActionsService.get_contact_to_call_alert().count(),
            "count_call_after_meet_advice": RequiredActionsService.get_call_after_meet_alert().count(),
            "count_payment_request": RequiredActionsService.get_payment_request_alert().count(),
            "count_ANAH": RequiredActionsService.get_ANAH_delay_alert().count(),
        }

    @staticmethod
    def fetch_reported_projects(
        page=PROJECTS_DEFAULT_PAGE,
        size=PROJECTS_DEFAULT_PAGE_SIZE,
        sort_by=PROJECTS_DEFAULT_SORT_FIELD,
        direction=PROJECTS_DEFAULT_SORT_DIRECTION,
        alert_type: str = None,
    ) -> Pagination:

        base_q = RequiredActionsService.create_base_actions_query(
            sort_by=sort_by, direction=direction
        )
        if alert_type == "count_meet_advices_to_plan":
            q = RequiredActionsService.get_meet_advices_to_plan_alert(base_q=base_q)
        elif alert_type == "count_meet_to_process":
            q = RequiredActionsService.get_meet_to_process_alert(base_q=base_q)
        elif alert_type == "count_contact_to_call_again":
            q = RequiredActionsService.get_contact_to_call_alert(base_q=base_q)
        elif alert_type == "count_call_after_meet_advice":
            q = RequiredActionsService.get_call_after_meet_alert(base_q=base_q)
        elif alert_type == "count_payment_request":
            q = RequiredActionsService.get_payment_request_alert(base_q=base_q)
        elif alert_type == "count_ANAH":
            q = RequiredActionsService.get_ANAH_delay_alert(base_q=base_q)
        else:
            raise InvalidSearchFieldException()

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_meet_advices_to_plan_alert(base_q=None):
        # Return query for projects having a Meet advices to plan alert
        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()

        visits_to_plan_status = [
            ProjectStatus.MEET_ADVICES_TO_PLAN.value,
            ProjectStatus.MEET_CONTROL_TO_PLAN.value,
        ]

        return projects_service.ProjectService.filter_query_project(
            q=base_q, project_status=visits_to_plan_status
        )

    @staticmethod
    def get_meet_to_process_alert(base_q=None):
        # Return query for projects having a Meet to process alert
        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()

        return projects_service.ProjectService.filter_query_project(
            user=g.user,
            q=base_q,
            project_status=ProjectStatus.MEET_TO_PROCESS.value,
            filter_on_referrer=True,
        )

    @staticmethod
    def get_contact_to_call_alert(base_q=None):
        # Return query for projects having a "Contact to call" alert
        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()

        today = date.today()
        date_2_months = today - dateutil.relativedelta.relativedelta(months=2)

        return projects_service.ProjectService.filter_query_project(
            user=g.user, q=base_q, project_status=ProjectStatus.CONTACT.value,
        ).filter(Project.updated_at < date_2_months)

    @staticmethod
    def get_call_after_meet_alert(base_q=None):
        # Return a query for projects having a "call after meet" alert

        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()

        today = date.today()
        date_2_months = today - dateutil.relativedelta.relativedelta(months=2)

        return projects_service.ProjectService.filter_query_project(
            user=g.user,
            q=base_q,
            project_status=ProjectStatus.BUILD_ON_GOING.value,
            filter_on_referrer=True,
        ).filter(Project.updated_at < date_2_months)

    @staticmethod
    def get_payment_request_alert(base_q=None):
        # Return query for projects having a "Payment request" alert
        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()

        return projects_service.ProjectService.filter_query_project(
            user=g.user,
            q=base_q,
            project_status=ProjectStatus.PAYMENT_REQUEST_TO_DO.value,
            filter_on_referrer=True,
        )

    @staticmethod
    def get_ANAH_delay_alert(base_q=None):
        # Return query for projects having a ANAH delay alert

        projects = RequiredActionsService.prefilter_projects_for_ANAH_alerts(
            base_q=base_q
        )
        reported_projects_id = []
        for project in projects:
            funder_raises_alert = False
            for funder in project.mission.funders:

                if RequiredActionsService.funder_raises_alert(project, funder):
                    funder_raises_alert = True
                    break

            if funder_raises_alert:
                reported_projects_id.append(project.id)

        # Retrieve the result
        filters_on_projects_id = (
            [
                Project.id == project_id
                for project_id in reported_projects_id
                if project_id
            ]
            if reported_projects_id
            else [False]
        )
        return Project.query.filter(or_(*filters_on_projects_id))

    @staticmethod
    def prefilter_projects_for_ANAH_alerts(base_q=None):
        # For current user, fetch all projects that could potentially raise an alert
        if not base_q:
            base_q = RequiredActionsService.create_base_actions_query()
        q = projects_service.ProjectService.filter_query_project(
            user=g.user,
            q=base_q,
            project_status_to_skip=[
                ProjectStatus.DISMISSED.value,
                ProjectStatus.NON_ELIGIBLE.value,
            ],
            filter_on_referrer=True,
        )
        q = q.filter(not_(Project.no_advance_request.is_(True)))
        return q.all()

    @staticmethod
    def funder_raises_alert(project, funder):
        # Return TRUE if provided funder within a project should raise an advance or payment alert

        certification_date = FunderMonitoringValue.get_automatic_value(
            project, funder, "Agrément"
        )
        if not certification_date:
            return False
        certification_delay = (datetime.today().date() - certification_date).days

        # Check advance alert
        if RequiredActionsService.has_funder_advance_alert(
            project, funder, certification_delay
        ):
            return True
        # Check payment alert
        if RequiredActionsService.has_funder_payment_alert(
            project, funder, certification_delay
        ):
            return True

        return False

    @staticmethod
    def has_funder_advance_alert(project, funder, certification_delay):
        # Return True if a funder has expired date for advance
        funder_monitoring_value_advance = (
            FunderMonitoringValue.query.filter(
                FunderMonitoringValue.project_id == project.id
            )
            .filter(FunderMonitoringValue.funder_id == funder.id)
            .filter(
                FunderMonitoringValue.monitor_field.has(MonitorField.name == "Avance")
            )
        ).first()

        advance_date = (
            funder_monitoring_value_advance.value
            if funder_monitoring_value_advance is not None
            else None
        )

        return (
            advance_date is None
            and project.mission.monitor.advance_alert is not None
            and certification_delay > project.mission.monitor.advance_alert
        )

    @staticmethod
    def has_funder_payment_alert(project, funder, certification_delay):
        # Return True if a funder has expired date for payment request
        payment_request_date = FunderMonitoringValue.get_automatic_value(
            project, funder, "Envoi demande de paiement"
        )
        return (
            payment_request_date is None
            and certification_delay
            and project.mission.monitor.payment_alert
            and certification_delay > project.mission.monitor.payment_alert
        )

    @staticmethod
    def create_base_actions_query(sort_by=None, direction=None):
        q = projects_service.ProjectService.filter_query_project(
            user=g.user, q=Project.query,
        )
        return (
            sort_query(q, sort_by, direction)
            if sort_by is not None and direction is not None
            else q
        )
