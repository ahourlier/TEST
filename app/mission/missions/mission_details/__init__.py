from flask_restx import Namespace
from .model import MissionDetail
from .schema import MissionDetail


api = Namespace("MissionDetails", description="Mission details namespace")
