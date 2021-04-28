from .model import Mission

from flask_restx import Namespace

from .schema import MissionSchema

api = Namespace("Missions", description="Missions namespace")
