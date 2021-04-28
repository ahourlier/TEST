from . import api, CommonAreaSchema, CommonArea
from flask import request, Response, jsonify

from flask_accepts import accepts, responds

from .interface import CommonAreaInterface
from .service import CommonAreaService
from ...common.api import AuthenticatedApi


@api.route("/project/<int:project_id>")
@api.param("projectId", "Project unique ID")
class CommonAreaResource(AuthenticatedApi):
    @accepts(schema=CommonAreaSchema(), api=api)
    @responds(schema=CommonAreaSchema(), api=api)
    def post(self, project_id) -> CommonArea:
        """ Create an common_area """
        return CommonAreaService.create(request.parsed_obj, project_id)


@api.route("/<int:common_area_id>")
@api.param("commonAreaId", "CommonArea unique ID")
class CommonAreaIdResource(AuthenticatedApi):
    @responds(schema=CommonAreaSchema(), api=api)
    def get(self, common_area_id: int) -> CommonArea:
        """ Get single common_area """

        return CommonAreaService.get_by_id(common_area_id)

    def delete(self, common_area_id: int) -> Response:
        """Delete single common_area"""

        id = CommonAreaService.delete_by_id(common_area_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=CommonAreaSchema(), api=api)
    @responds(schema=CommonAreaSchema(), api=api)
    def put(self, common_area_id: int) -> CommonArea:
        """Update single common_area"""

        changes: CommonAreaInterface = request.parsed_obj
        db_common_area = CommonAreaService.get_by_id(common_area_id)
        return CommonAreaService.update(db_common_area, changes)
