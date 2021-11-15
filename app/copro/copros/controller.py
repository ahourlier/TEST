import os

from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from flask_restx import inputs
from . import api
# from . import api, Mission
# from .interface import MissionInterface
# from .mission_details.interface import MissionDetailInterface
# from .mission_details.schema import MissionDetailSchema
# from .mission_details.service import MissionDetailService
# from .schema import (
#     MissionPaginatedSchema,
#     MissionSchema,
#     MissionDocumentSchema,
#     MissionCreateSchema,
# )
# from .service import (
#     MissionService,
#     MISSIONS_DEFAULT_PAGE,
#     MISSIONS_DEFAULT_PAGE_SIZE,
#     MISSIONS_DEFAULT_SORT_FIELD,
#     MISSIONS_DEFAULT_SORT_DIRECTION,
#     MISSION_INIT_QUEUE_NAME,
# )
from .schema import CoproPaginatedSchema
from .service import CoproService, COPRO_DEFAULT_PAGE, COPRO_DEFAULT_PAGE_SIZE, COPRO_DEFAULT_SORT_DIRECTION, \
    COPRO_DEFAULT_SORT_FIELD
from ... import db
from ...admin.subcontractor.service import SubcontractorService
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
class CoprosResource(AuthenticatedApi):
    """ Coproprietes """

    @accepts(
        *SEARCH_PARAMS,
        api=api,
    )
    @responds(schema=CoproPaginatedSchema(), api=api)
    def get(self) -> Pagination:
        """ Get all missions """
        return CoproService.get_all(
            page=int(request.args.get("page", COPRO_DEFAULT_PAGE)),
            size=int(request.args.get("size", COPRO_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", COPRO_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", COPRO_DEFAULT_SORT_DIRECTION
            ),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
        )
