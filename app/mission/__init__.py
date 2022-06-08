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
    from .missions.mission_details.job.controller import api as job_api
    from .missions.mission_details.subjob.controller import api as subjob_api
    from .missions.mission_details.operational_plan.controller import (
        api as operational_plans_api,
    )
    from .missions.mission_details.partner.controller import api as partner_api
    from .missions.mission_details.elect.controller import api as elect_api
    from .missions.mission_details.financial_device.controller import (
        api as financial_device_api,
    )

    api.add_namespace(missions_api, path=f"/{root}/{BASE_ROUTE}/missions")
    api.add_namespace(teams_api, path=f"/{root}/{BASE_ROUTE}/teams")
    api.add_namespace(custom_fields_api, path=f"/{root}/{BASE_ROUTE}/custom_fields")
    api.add_namespace(monitors_api, path=f"/{root}/{BASE_ROUTE}/monitors")
    api.add_namespace(job_api, path=f"/{root}/jobs")
    api.add_namespace(subjob_api, path=f"/{root}/subjobs")
    api.add_namespace(operational_plans_api, path=f"/{root}/operational_plans")
    api.add_namespace(partner_api, path=f"/{root}/partners")
    api.add_namespace(elect_api, path=f"/{root}/elects")
    api.add_namespace(financial_device_api, path=f"/{root}/financial_device")


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
