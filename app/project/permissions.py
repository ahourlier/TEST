from enum import Enum

from flask import g
from sqlalchemy.sql.elements import or_, and_

import app.project.projects.service as projects_service
import app.mission.missions.service as missions_service
import app.mission.permissions as missions_permissions
from app.auth.users.model import UserRole
from app.mission.missions import Mission
from app.mission.teams import Team
from app.mission.teams.model import UserTeamPositions

import app.common.permissions as permissions_utils
from app.project.projects import Project


PROJECT_FIELDS_AUTHORIZATIONS_MAP = {
    "base": [
        "id",
        "sections_permissions",
        "mission_name",
        "code_name",
        "requester_light",
        "status",
        "anonymized",
        "work_types",
        "mission_id",
    ],
    "ca_requester": [
        "address",
        "type",
        "work_type",
        "description",
        "closed",
        "closure_motive",
        "urgent_visit",
        "date_advice_meet",
        "date_control_meet",
        "date_control_meet",
        "notes",
        "mission_id",
        "date_meet_advices_to_plan",
        "date_meet_control_to_plan",
        "date_to_contact",
        "date_contact",
        "date_meet_to_process",
        "date_build_on_going",
        "date_depositted",
        "date_certified",
        "date_meet_advices_planned",
        "date_meet_control_planned",
        "date_payment_request_to_do",
        "date_asking_for_pay",
        "date_cleared",
        "date_dismissed",
        "date_non_eligible",
        "requester_id",
        "requester",
        "referrers",
    ],
    "ca_accommodation": [
        "accommodation",
        "accommodations_length",
        "common_areas",
        "work_types",
    ],
    "ca_common_area": ["common_areas"],
    "ca_accommodation_summary": [],
    "ca_quotes": [],
    "ca_simulations": [],
    "ca_deposit": [],
    "ca_certification": [],
    "ca_payment_request": [],
    "ca_funders": ["monitoring_commentary", "no_advance_request"],
    "ca_documents": [],
    "ca_follow_up": [],
}


class ProjectPermission:
    @staticmethod
    def check_project_permission(
        user, project_id, include_client_access=False, app_section=None
    ):
        """Return True if user has the authorization to access the given project.
        By default, does not include specific clients accesses.
        By default, does not specify an app section for client accesses"""
        project = projects_service.ProjectService.get_by_id(project_id)
        if not project_id:
            # Project_id is not provided. Only admin has access to the road.
            return user.role == UserRole.ADMIN
        has_mission_permission = missions_permissions.MissionPermission.check_mission_permission(
            project.mission_id, user
        )
        has_permission = permissions_utils.PermissionsUtils.bypass_admins(
            has_mission_permission, user
        )
        if include_client_access:
            client_permission = missions_permissions.MissionPermission.has_client_mission_access(
                project.mission_id, user, app_section
            )
            return has_permission or client_permission
        else:
            return has_permission

    @staticmethod
    def query_project_remove_unauthorized(q, user):
        """Remove unauthorized projects with default parameters :
        - Take accounts of clients access
        - Always authorize for admins and managers"""
        q = ProjectPermission.filter_query_project_by_user_permissions(q, user)
        q = ProjectPermission.filter_project_by_app_section_access(q, user)
        return q

    @staticmethod
    def filter_query_project_by_user_permissions(q, user, bypass_admins=True):
        """Filter a project query by user permission, including client accesses"""
        if bypass_admins and user.role == UserRole.ADMIN:
            return q

        user_agencies = [group.agency_id for group in user.groups if group.agency_id]
        user_antennas = [group.antenna_id for group in user.groups if group.antenna_id]
        q = q.filter(
            Project.mission.has(
                Mission.teams.any(
                    or_(
                        Team.user_id == user.id,
                        Team.antenna_id.in_(user_antennas),
                        Team.agency_id.in_(user_agencies),
                    )
                )
            )
        )

        return q

    @staticmethod
    def filter_project_by_app_section_access(q, user):
        """If user is client, filter query on app sections accesses configured at mission level"""
        if user.role != UserRole.CLIENT:
            return q
        return q.filter(
            Project.mission.has(
                and_(
                    Mission.teams.any(
                        Team.user_id == user.id
                        and Team.user_position == UserTeamPositions.CLIENT_ACCESS.value,
                    ),
                    or_(
                        Mission.ca_requester == True,
                        Mission.ca_accommodation == True,
                        Mission.ca_common_area == True,
                        Mission.ca_accommodation_summary == True,
                        Mission.ca_quotes == True,
                        Mission.ca_simulations == True,
                        Mission.ca_deposit == True,
                        Mission.ca_certification == True,
                        Mission.ca_payment_request == True,
                        Mission.ca_funders == True,
                        Mission.ca_documents == True,
                        Mission.ca_funders == True,
                        Mission.ca_follow_up == True,
                    ),
                )
            )
        )

    @staticmethod
    def filter_project_fields(response):
        """Callback for "filter_response_with_clients_access" decorator.
        Extract forbidden fields from a project item, according to clients access permissions"""
        filtered_response = list(response)
        if g.user.role == UserRole.CLIENT:
            filtered_response[
                0
            ] = missions_permissions.MissionPermission.filter_item_response_by_mission_settings(
                response[0],
                ProjectPermission.extract_mission_id_from_project,
                fields_access_map=PROJECT_FIELDS_AUTHORIZATIONS_MAP,
            )
        return tuple(filtered_response)

    @staticmethod
    def filter_projects_list_fields(response):
        """Callback for "filter_response_with_clients_access" decorator.
        Extract forbidden fields from a projects list, according to clients access permissions"""
        if g.user.role == UserRole.CLIENT:
            items = missions_permissions.MissionPermission.filter_list_response_by_mission_settings(
                response[0].get("items"),
                ProjectPermission.extract_mission_id_from_project,
                fields_access_map=PROJECT_FIELDS_AUTHORIZATIONS_MAP,
            )
            response[0]["items"] = items
        return response

    @staticmethod
    def extract_mission_id_from_project(project):
        """Callback used during client access decorator workflow"""
        return project.get("mission_id")
