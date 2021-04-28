from .model import Team

from flask_restx import Namespace

from .schema import TeamSchema

api = Namespace("Teams", description="Teams namespace")
