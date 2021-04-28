from app.mission.missions.internal_controller import (
    MissionsInitDriveView,
    MissionInitPermissions,
    MissionAddMember,
    MissionRemoveMember,
    MissionComputePermissions,
)

BASE_ROUTE = "mission"


def register_routes(api, app, root="api"):
    from .missions.controller import api as missions_api
    from .teams.controller import api as teams_api
    from .custom_fields.controller import api as custom_fields_api
    from .monitors.controller import api as monitors_api

    api.add_namespace(missions_api, path=f"/{root}/{BASE_ROUTE}/missions")
    api.add_namespace(teams_api, path=f"/{root}/{BASE_ROUTE}/teams")
    api.add_namespace(custom_fields_api, path=f"/{root}/{BASE_ROUTE}/custom_fields")
    api.add_namespace(monitors_api, path=f"/{root}/{BASE_ROUTE}/monitors")


def register_internal_routes(bp):
    prefix = "/missions"
    bp.add_url_rule(
        f"{prefix}/init-drive",
        view_func=MissionsInitDriveView.as_view("mission-init-drive"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/init-permissions",
        view_func=MissionInitPermissions.as_view("mission-init-permissions"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/add-member",
        view_func=MissionAddMember.as_view("mission-add-member"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/remove-member",
        view_func=MissionRemoveMember.as_view("mission-remove-member"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/compute-permissions",
        view_func=MissionComputePermissions.as_view("mission-compute-permissions"),
        methods=["POST"],
    )
