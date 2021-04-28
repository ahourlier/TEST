import logging
from enum import Enum
from typing import List

from flask import g
from sqlalchemy.sql.elements import or_

import app.mission.missions.service as missions_service
import app.common.permissions as permissions_utils
from app.auth.users.model import UserRole
from app.mission.missions import Mission
from app.mission.teams import Team
from app.mission.teams.model import UserTeamPositions


MISSION_CLIENT_AUTHORIZED_FIELDS = ["id", "name"]


class ProjectSectionsAccess(Enum):

    REQUESTER = "ca_requester"
    ACCOMMODATION = "ca_accommodation"
    COMMON_AREA = "ca_common_area"
    ACCOMMODATION_SUMMARY = "ca_accommodation_summary"
    QUOTES = "ca_quotes"
    SIMULATIONS = "ca_simulations"
    DEPOSIT = "ca_deposit"
    CERTIFICATION = "ca_certification"
    PAYMENT_REQUEST = "ca_payment_request"
    FUNDERS = "ca_funders"
    DOCUMENTS = "ca_documents"
    FOLLOW_UP = "ca_follow_up"


class MissionPermission:
    @staticmethod
    def check_mission_permission(mission_id: int, user):
        """ Return True if user has a personal access to a given mission """
        accesses = MissionPermission.fetch_mission_access_list(mission_id, user)
        return len(accesses) > 0

    @staticmethod
    def fetch_mission_access_list(mission_id: int, user):
        """ Return the list of user accesses to a given mission. (but not "clients accesses", which are checked in
        another method """
        mission = missions_service.MissionService.get_by_id(mission_id)
        user_roles = []

        # Fetch other roles, linked to the mission's teams
        user_agencies = [group.agency_id for group in user.groups if group.agency_id]
        user_antennas = [group.antenna_id for group in user.groups if group.antenna_id]

        for team in mission.teams:
            if (
                (
                    user.id == team.user_id
                    and team.user_position != UserTeamPositions.CLIENT_ACCESS
                )
                or team.antenna_id in user_antennas
                or team.agency_id in user_agencies
            ):
                user_roles.append(team.user_position)

        return user_roles

    @staticmethod
    def has_client_mission_access(mission_id: int, user, app_section=None):
        """Return True if user has a client_access set for this mission.
         The 'app_section' params allows to filter by one specific app_section access """
        if app_section and app_section not in ProjectSectionsAccess.__members__:
            return False
        mission = missions_service.MissionService.get_by_id(mission_id)
        for team in mission.teams:
            if app_section:
                mission_authorizes_section = getattr(mission, app_section)
                if (
                    mission_authorizes_section
                    and user.id == team.user_id
                    and team.user_position == UserTeamPositions.CLIENT_ACCESS
                ):
                    return True
            else:
                if (
                    user.id == team.user_id
                    and team.user_position == UserTeamPositions.CLIENT_ACCESS
                ):
                    return True

        return False

    @staticmethod
    def filter_query_mission_by_user_permissions(q, user, bypass_admins=True):
        """Filter a mission query by user permission, including client accesses"""
        if bypass_admins and user.role == UserRole.ADMIN:
            return q

        user_agencies = [group.agency_id for group in user.groups if group.agency_id]
        user_antennas = [group.antenna_id for group in user.groups if group.antenna_id]
        q = q.filter(
            Mission.teams.any(
                or_(
                    Team.user_id == user.id,
                    Team.antenna_id.in_(user_antennas),
                    Team.agency_id.in_(user_agencies),
                )
            )
        )

        return q

    @staticmethod
    def filter_item_response_by_mission_settings(
        response,
        extract_mission_id_func,
        fields_access_map: dict = None,
        authorized_fields: List = None,
    ):
        """ Remove forbidden fields from a unique item response.
        Meant to be used within an endpoint decorator
        fields_access_map : a dictionnary used to build an authorized_fields list according to mission client access settings
        authorized_fields : a list of authorized_fields in order to filter the response."""
        mission_id = extract_mission_id_func(response)
        mission = missions_service.MissionService.get_by_id(mission_id)
        if not authorized_fields:
            authorized_fields = permissions_utils.PermissionsUtils.determine_authorized_fields(
                mission, fields_access_map
            )
        filtered_response = permissions_utils.PermissionsUtils.remove_fields_from_response(
            response, authorized_fields
        )
        return filtered_response

    @staticmethod
    def filter_list_response_by_mission_settings(
        response,
        extract_mission_id_func,
        fields_access_map: dict = None,
        authorized_fields: List = None,
    ):
        """ Remove forbidden fields from a list of items.
        Meant to be used within an endpoint decorator
        fields_access_map : a dictionnary used to build an authorized_fields list according to mission client access settings
        authorized_fields : a list of authorized_fields in order to filter the response.
        """
        if not authorized_fields and not fields_access_map:
            logging.error("No map given to endpoint filter. Response is not filtered")
            return response
        missions_reference = {}
        filtered_response = []
        for item in response:
            mission_id = extract_mission_id_func(item)
            if mission_id not in missions_reference:
                mission = missions_service.MissionService.get_by_id(mission_id)
                missions_reference[mission_id] = mission
            mission = missions_reference.get(mission_id)
            if not authorized_fields:
                authorized_fields = permissions_utils.PermissionsUtils.determine_authorized_fields(
                    mission, fields_access_map
                )
            filtered_item = permissions_utils.PermissionsUtils.remove_fields_from_response(
                item, authorized_fields
            )
            filtered_response.append(filtered_item)

        return filtered_response

    @staticmethod
    def filter_missions_list_fields(response):
        """ Callback for "filter_response_with_clients_access" decorator.
         Extract forbidden fields from a missions list, according to clients access permissions"""

        if g.user.role == UserRole.CLIENT:
            items = MissionPermission.filter_list_response_by_mission_settings(
                response[0].get("items"),
                MissionPermission.extract_mission_id_from_project,
                authorized_fields=MISSION_CLIENT_AUTHORIZED_FIELDS,
            )
            response[0]["items"] = items
        return response

    @staticmethod
    def extract_mission_id_from_project(mission):
        """ Callback used during client access decorator workflow"""
        return mission.get("id")
