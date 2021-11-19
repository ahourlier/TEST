import functools
from enum import Enum

from flask import request, g

from app.funder.funders.service import FunderService
from app.auth.users.model import UserRole
from app.funder.funding_scenarios.service import FundingScenarioService
import app.project.permissions as project_permissions
import app.mission.permissions as mission_permissions
import app.mission.missions.service as missions_service


class PermissionsUtils:
    @staticmethod
    def get_entity_id(key, sub_key=None, fallback=None):
        """Extract a targeted id from a raw request."""
        entity_id = None
        if request.view_args.get(key) is not None:
            entity_id = request.view_args.get(key)
        elif request.args.get(key) is not None:
            entity_id = request.args.get(key)
        elif (
            request.json is not None
            and hasattr(request, "parsed_obj")
            and request.parsed_obj.get(key) is not None
        ):
            entity_id = PermissionsUtils.get_entity_id_into_body(
                key, sub_key, request.parsed_obj
            )

        return entity_id if entity_id is not None else fallback

    @staticmethod
    def get_entity_id_into_body(key, sub_key, payload):
        """Extract a targeted id (or a sub_key) from a request body."""
        key_value = payload.get(key)
        if not key_value:
            return None
        if isinstance(key_value, list) and sub_key:
            entities_id = [value.get(sub_key) for value in key_value]
            if None in entities_id:
                return None
            return entities_id
        return key_value

    @staticmethod
    def bypass_admins(local_permission, user):
        # Return the given permission boolean if user has no overrinding global role, else True.
        # Allow to bypass specifics/locals access by global admins or managers access
        return True if user.role == UserRole.ADMIN else local_permission

    @staticmethod
    def determine_authorized_fields(mission, fields_map):
        authorized_fields = []
        for key, value in fields_map.items():
            if key == "base" or getattr(mission, key) is True:
                authorized_fields.extend(fields_map.get(key))
        return authorized_fields

    @staticmethod
    def remove_fields_from_response(response, authorized_fields):
        if not authorized_fields:
            return response
        for field in response.copy():
            if field not in authorized_fields:
                del response[field]
        return response


def is_admin(user):
    return user.role == UserRole.ADMIN


def is_manager(user):
    return user.role in [UserRole.ADMIN, UserRole.MANAGER]


def is_contributor(user):
    return user.role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.CONTRIBUTOR]


def is_client(user):
    return user.role in [
        UserRole.ADMIN,
        UserRole.MANAGER,
        UserRole.CONTRIBUTOR,
        UserRole.CLIENT,
    ]


def has_mission_permission(user):
    mission_id = PermissionsUtils.get_entity_id("mission_id")
    if not mission_id:
        # Mission_id is not provided. Only admin has access to the road.
        return user.role == UserRole.ADMIN
    missions_service.MissionService.get_by_id(mission_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_copro_permission(user):
    mission_id = PermissionsUtils.get_entity_id("missionId")
    missions_service.MissionService.get_by_id(mission_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_project_permission(user):
    project_id = PermissionsUtils.get_entity_id("project_id")
    return project_permissions.ProjectPermission.check_project_permission(
        user, project_id
    )


def has_project_employee_or_client_permission(user):
    project_id = PermissionsUtils.get_entity_id("project_id")
    return project_permissions.ProjectPermission.check_project_permission(
        user, project_id, include_client_access=True
    )


def has_multiple_projects_permission(user):
    projects_id = PermissionsUtils.get_entity_id("projects_id")
    for project_id in projects_id:
        if (
            project_permissions.ProjectPermission.check_project_permission(
                user, project_id
            )
            is False
        ):
            return False
    return True


def can_manage_funders(user):
    """
    Check if a user can create/update/delete a funder or a funding scenario
    If not mission_id needs to be admin, else needs to be admin
    """

    funder_id = PermissionsUtils.get_entity_id("funder_id")
    funding_scenario_id = PermissionsUtils.get_entity_id("funding_scenario_id")
    mission_id = PermissionsUtils.get_entity_id("mission_id")

    if mission_id is not None:
        return user.role in [UserRole.ADMIN, UserRole.MANAGER]
    if funding_scenario_id is not None:
        db_funding_scenario = FundingScenarioService.get_by_id(funding_scenario_id)
        return (
            user.role in [UserRole.ADMIN, UserRole.MANAGER]
            if not db_funding_scenario.funder.is_national
            else user.role == UserRole.ADMIN
        )
    if funder_id is not None:
        funder = FunderService.get_by_id(funder_id)
        return (
            user.role in [UserRole.ADMIN, UserRole.MANAGER]
            if not funder.is_national
            else user.role == UserRole.ADMIN
        )

    return user.role == UserRole.ADMIN


def filter_response_with_clients_access(filter_func):
    """ Decorator that filters responses objects according to mission settings """

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            response = func(*args, **kwargs)
            if g.user.role != UserRole.CLIENT:
                return response
            response = filter_func(response)
            return response

        return wrapped_func

    return wrap
