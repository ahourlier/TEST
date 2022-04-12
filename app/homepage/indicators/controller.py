from flask import request

from flask_accepts import responds, accepts

from . import api
from .schema import IndicatorSchema, IndicatorFilterSchema
from .service import IndicatorService
from ...common.api import AuthenticatedApi


@api.route("/")
class IndicatorResource(AuthenticatedApi):
    @accepts(
        dict(name="mission_id", type=int),
        dict(name="requester_type", type=str),
        api=api,
    )
    @responds(schema=IndicatorSchema(), api=api)
    def get(self):
        """Get indicator data"""

        return IndicatorService.get(
            missions_id=int(request.args.get("mission_id"))
            if request.args.get("mission_id") not in [None, ""]
            else None,
            requester_type=str(request.args.get("requester_type"))
            if request.args.get("requester_type") not in [None, ""]
            else None,
        )

    @accepts(schema=IndicatorFilterSchema, api=api)
    @responds(schema=IndicatorSchema)
    def post(self):
        """Get indicator data with filter on multiple missions_id"""
        return IndicatorService.get(missions_id=request.parsed_obj.get("missions_id"))
