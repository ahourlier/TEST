import os

from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from flask_restx import inputs

from . import api, Mission
from .interface import MissionInterface
from .mission_details.interface import MissionDetailInterface
from .mission_details.schema import MissionDetailSchema
from .mission_details.service import MissionDetailService
from .mission_details.subcontractor.service import SubcontractorService
from .schema import (
    MissionPaginatedSchema,
    MissionSchema,
    MissionDocumentSchema,
    MissionCreateSchema,
)
from .service import (
    MissionService,
    MISSIONS_DEFAULT_PAGE,
    MISSIONS_DEFAULT_PAGE_SIZE,
    MISSIONS_DEFAULT_SORT_FIELD,
    MISSIONS_DEFAULT_SORT_DIRECTION,
    MISSION_INIT_QUEUE_NAME,
)
from ... import db
from ...auth.users.service import UserService
from ...common.api import AuthenticatedApi
from ...common.app_name import App
from ...common.permissions import (
    is_manager,
    is_contributor,
    is_admin,
    filter_response_with_clients_access,
    has_mission_permission,
)
from ...common.search import SEARCH_PARAMS
import app.mission.permissions as missions_permissions
from ...common.tasks import create_task


@api.route("/")
class MissionResource(AuthenticatedApi):
    """ Missions """

    @filter_response_with_clients_access(
        missions_permissions.MissionPermission.filter_missions_list_fields
    )
    @accepts(
        *SEARCH_PARAMS,
        dict(name="agency_id", type=int),
        dict(name="antenna_id", type=int),
        dict(name="client_id", type=int),
        api=api,
    )
    @responds(schema=MissionPaginatedSchema(), api=api)
    def get(self) -> Pagination:
        """ Get all missions """
        return MissionService.get_all(
            page=int(request.args.get("page", MISSIONS_DEFAULT_PAGE)),
            size=int(request.args.get("size", MISSIONS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", MISSIONS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", MISSIONS_DEFAULT_SORT_DIRECTION
            ),
            agency_id=int(request.args.get("agency_id"))
            if request.args.get("agency_id") not in [None, ""]
            else None,
            antenna_id=int(request.args.get("antenna_id"))
            if request.args.get("antenna_id") not in [None, ""]
            else None,
            client_id=int(request.args.get("client_id"))
            if request.args.get("client_id") not in [None, ""]
            else None,
            user=g.user,
            mission_type=request.args.get("missionType")
            if request.args.get("missionType") not in [None, ""]
            else None,
        )

    @accepts(schema=MissionCreateSchema(), api=api)
    @responds(schema=MissionSchema(), api=api)
    @requires(is_manager)
    def post(self) -> Mission:
        """ Create a mission """
        return MissionService.create(request.parsed_obj)


@api.route("/<int:mission_id>")
@api.param("missionId", "Mission unique ID")
class MissionIdResource(AuthenticatedApi):
    @responds(schema=MissionSchema(), api=api)
    @accepts(dict(name="check_drive_structure", type=inputs.boolean))
    @requires(is_contributor)
    def get(self, mission_id: int) -> Mission:
        """ Get single mission """
        db_mission = MissionService.get_by_id(mission_id)

        if db_mission.mission_type == App.INDIVIDUAL:
            check_drive_structure = (
                True
                if request.args.get("check_drive_structure", "true").lower() == "true"
                else False
            )

            if (
                db_mission.drive_init not in ["IN PROGRESS", "DONE"]
                and check_drive_structure
            ):
                if (
                    db_mission.sd_root_folder_id
                    and db_mission.sd_projects_folder_id
                    and db_mission.sd_document_templates_folder_id
                    and db_mission.sd_information_documents_folder_id
                    and db_mission.google_group_id
                ):
                    db_mission.drive_init = "DONE"
                    db.session.commit()
                else:
                    db_mission.drive_init = "IN PROGRESS"
                    db.session.commit()
                    create_task(
                        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                        location=os.getenv("QUEUES_LOCATION"),
                        queue=MISSION_INIT_QUEUE_NAME,
                        uri=f"{os.getenv('API_URL')}/_internal/missions/init-drive",
                        method="POST",
                        payload={"mission_id": db_mission.id,},
                    )
        return db_mission

    @requires(is_manager)
    def delete(self, mission_id: int) -> Response:
        """Delete single mission"""

        id = MissionService.delete_by_id(mission_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=MissionSchema(), api=api)
    @responds(schema=MissionSchema(), api=api)
    @requires(has_mission_permission)
    def put(self, mission_id: int) -> Mission:
        """Update single mission"""

        changes: MissionInterface = request.parsed_obj
        db_mission = MissionService.get_by_id(mission_id)
        return MissionService.update(db_mission, changes)


@api.route("/user/<int:user_id>")
@api.param("userId", "User unique ID")
class MissionByUserResource(AuthenticatedApi):
    @accepts(
        *SEARCH_PARAMS,
        dict(name="agency_id", type=int),
        dict(name="antenna_id", type=int),
        dict(name="client_id", type=int),
        api=api,
    )
    @responds(schema=MissionPaginatedSchema(), api=api)
    @requires(is_admin)
    def get(self, user_id: int) -> Pagination:
        """ Get missions filtered by user """
        user = UserService.get_by_id(user_id)
        return MissionService.get_all(
            page=int(request.args.get("page", MISSIONS_DEFAULT_PAGE)),
            size=int(request.args.get("size", MISSIONS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", MISSIONS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", MISSIONS_DEFAULT_SORT_DIRECTION
            ),
            agency_id=int(request.args.get("agency_id"))
            if request.args.get("agency_id") not in [None, ""]
            else None,
            antenna_id=int(request.args.get("antenna_id"))
            if request.args.get("antenna_id") not in [None, ""]
            else None,
            client_id=int(request.args.get("client_id"))
            if request.args.get("client_id") not in [None, ""]
            else None,
            user=user,
            mission_type=request.args.get("missionType")
            if request.args.get("missionType") not in [None, ""]
            else None,
        )


@api.route("/<int:mission_id>/documents")
@api.param("missionId", "Mission unique ID")
class MissionDocumentResource(AuthenticatedApi):
    @accepts(schema=MissionDocumentSchema, api=api)
    @requires(is_contributor)
    def post(self, mission_id: int):
        db_mission = MissionService.get_by_id(mission_id)
        data = request.parsed_obj
        resp = MissionService.add_document(
            db_mission, data.get("files_id"), data.get("kind"), g.user.email
        )
        return jsonify(resp)


@api.route("/<int:mission_id>/details")
@api.param("missionId", "Mission unique ID")
class MissionDetailsResource(AuthenticatedApi):
    @responds(api=api)
    def get(self, mission_id: int):
        return MissionService.get_details_by_mission_id(mission_id)

    @responds(schema=MissionDetailSchema, api=api)
    @accepts(schema=MissionDetailSchema, api=api)
    def put(self, mission_id):
        changes: MissionDetailInterface = request.parsed_obj
        db_mission_details = MissionDetailService.get_by_mission_id(mission_id)
        return MissionDetailService.update(db_mission_details, changes)


@api.route("/<int:mission_id>/subcontractor/<int:subcontractor_id>")
@api.param("missionId", "Mission unique ID")
@api.param("subcontractorId", "Subcontractor ID")
class SubcontractorMissionResource(AuthenticatedApi):
    @responds(api=api)
    def post(self, mission_id, subcontractor_id):
        SubcontractorService.link(mission_id, subcontractor_id)
        return jsonify(
            dict(
                status="Success",
                mission_id=mission_id,
                subcontractor_id=subcontractor_id,
            )
        )

    @responds(api=api)
    def delete(self, mission_id, subcontractor_id):
        SubcontractorService.unlink(mission_id, subcontractor_id)
        return jsonify(
            dict(
                status="Success",
                mission_id=mission_id,
                subcontractor_id=subcontractor_id,
            )
        )
