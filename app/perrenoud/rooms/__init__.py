from flask_restx import Namespace
from .model import Room

#  from .schema import RoomSchema

api = Namespace("Rooms", description="Rooms namespace")
