from flask import request, g
from app.combined_structure.service import CombinedStructureService

from app.funder.funders.service import FunderService
from app.auth.users.model import UserRole
from app.funder.funding_scenarios.service import FundingScenarioService
import app.project.permissions as project_permissions
import app.mission.permissions as mission_permissions
import app.mission.missions.service as missions_service
import app.copro.copros.service as copro_service
import app.building.service as building_service
import app.lot.service as lot_service
import app.thematique.service as thematic_service
import app.v2_imports.service as import_service


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
    """Decorator that filters responses objects according to mission settings"""

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            response = func(*args, **kwargs)
            if g.user.role != UserRole.CLIENT:
                return response
            response = filter_func(response)
            return response

        return wrapped_func

    return wrap


# check permissions for route with id


def has_copro_permissions(user):
    copro_id = PermissionsUtils.get_entity_id("copro_id")
    if not copro_id:
        copro_id = PermissionsUtils.get_entity_id("coproId")
    if not copro_id:
        # copro_id is not provided. Only admin has access to the road.
        return user.role == UserRole.ADMIN
    return check_copro_permissions(copro_id, user)


def has_building_permissions(user):
    building_id = PermissionsUtils.get_entity_id("buildingId")
    if not building_id:
        building_id = PermissionsUtils.get_entity_id("building_id")
    building = building_service.BuildingService.get(building_id)
    if building:
        return check_copro_permissions(building.copro_id, user)


def has_lot_permissions(user):
    lot_id = PermissionsUtils.get_entity_id("lotId")
    if not lot_id:
        lot_id = PermissionsUtils.get_entity_id("lot_id")
    return check_lot_permissions(lot_id, user)


def has_mission_permission(user):
    mission_id = PermissionsUtils.get_entity_id("mission_id")
    if not mission_id:
        mission_id = PermissionsUtils.get_entity_id("missionId")

    if not mission_id:
        # Mission_id is not provided. Only admin has access to the road.
        return user.role == UserRole.ADMIN
    missions_service.MissionService.get_by_id(mission_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_task_permission(user):
    task_id = PermissionsUtils.get_entity_id("task_id")
    if not task_id:
        task_id = PermissionsUtils.get_entity_id("taskId")

    if not task_id:
        return user.role == UserRole.ADMIN
    from app.task.service import TaskService

    current_task = TaskService.get(task_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        current_task.mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_import_permissions(user):
    import_id = PermissionsUtils.get_entity_id("import_id")
    if not import_id:
        import_id = PermissionsUtils.get_entity_id("importId")

    if not import_id:
        return user.role == UserRole.ADMIN

    current_import = import_service.ImportsService.get(import_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        current_import.mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


# check permissions for list


def has_combined_structure_list_permissions(user):
    mission_id = PermissionsUtils.get_entity_id("missionId")
    if not mission_id:
        # Mission_id is not provided, filter will be done in logic
        return True
    missions_service.MissionService.get_by_id(mission_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_copro_list_permissions(user):
    mission_id = PermissionsUtils.get_entity_id("missionId")
    if not mission_id:
        # Mission_id is not provided, filter will be done in logic
        return True
    missions_service.MissionService.get_by_id(mission_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def has_building_list_permissions(user):
    mission_id = PermissionsUtils.get_entity_id("missionId")
    if mission_id:
        permission = mission_permissions.MissionPermission.check_mission_permission(
            mission_id, user
        )
        if not PermissionsUtils.bypass_admins(permission, user):
            return False
    copro_id = PermissionsUtils.get_entity_id("coproId")
    if copro_id:
        if not check_copro_permissions(copro_id, user):
            return False
    return True


def has_lot_list_permissions(user):
    mission_id = PermissionsUtils.get_entity_id("missionId")
    if mission_id:
        if not check_mission_permissions(mission_id, user):
            return False
    copro_id = PermissionsUtils.get_entity_id("coproId")
    if copro_id:
        if not check_copro_permissions(copro_id, user):
            return False
    building_id = PermissionsUtils.get_entity_id("buildingId")
    if building_id:
        if not check_building_permissions(building_id, user):
            return False
    return True


def has_combined_structure_permissions(user):
    cs_id = PermissionsUtils.get_entity_id("cs_id")
    if not cs_id:
        cs_id = PermissionsUtils.get_entity_id("csId")
    if not cs_id:
        return True
    return check_combined_structure_permissions(cs_id, user)


# check helpers


def check_combined_structure_permissions(cs_id, user):
    cs = CombinedStructureService.get(cs_id)
    return check_mission_permissions(cs.mission_id, user)


def check_mission_permissions(mission_id, user):
    permission = mission_permissions.MissionPermission.check_mission_permission(
        mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def check_copro_permissions(copro_id, user):
    copro = copro_service.CoproService.get(copro_id)
    permission = mission_permissions.MissionPermission.check_mission_permission(
        copro.mission_id, user
    )
    return PermissionsUtils.bypass_admins(permission, user)


def check_building_permissions(building_id, user):
    building = building_service.BuildingService.get(building_id)
    return check_copro_permissions(building.copro_id, user)


def check_lot_permissions(lot_id, user):
    lot = lot_service.LotService.get(lot_id)
    return check_copro_permissions(lot.copro_id, user)


# permissions for thematics


def has_thematic_permissions(user):
    resource_id = PermissionsUtils.get_entity_id("resourceId")
    if not resource_id:
        resource_id = PermissionsUtils.get_entity_id("resource_id")
    if not resource_id:
        return True
    scope = PermissionsUtils.get_entity_id("scope")
    return check_permissions_by_scope(scope, resource_id, user)


def has_version_permissions(user):
    version_id = PermissionsUtils.get_entity_id("version_id")
    version = thematic_service.ThematiqueService.get_version(version_id)
    return check_permissions_by_scope(
        version.get("scope"), version.get("resource_id"), user
    )


def check_permissions_by_scope(scope, resource_id, user):
    if scope == "sc":
        return check_combined_structure_permissions(resource_id, user)
    if scope == "copro":
        return check_copro_permissions(resource_id, user)
    if scope == "building":
        return check_building_permissions(resource_id, user)
    if scope == "lot":
        return check_lot_permissions(resource_id, user)
    return False
