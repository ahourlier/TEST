from flask_accepts import responds, accepts
from flask import request
from . import api
from .interface import RoomInterface
from .schema import RoomSchema
from .service import RoomService
from .. import Room
from ...common.api import AuthenticatedApi


@api.route("/<int:room_id>")
@api.param("roomId", "Room unique ID")
class RoomIdResource(AuthenticatedApi):
    @responds(schema=RoomSchema)
    def get(self, room_id: int) -> Room:
        """Get single room"""

        return RoomService.get_by_id(room_id)

    @accepts(schema=RoomSchema, api=api)
    @responds(schema=RoomSchema)
    def put(self, room_id: int) -> Room:
        """Update single room"""

        changes: RoomInterface = request.parsed_obj
        db_room = RoomService.get_by_id(room_id)
        return RoomService.update(db_room, changes)
