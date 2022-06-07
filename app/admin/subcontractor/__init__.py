from flask_restx import Namespace
from .model import MissionDetailSubcontractor, Subcontractor

api = Namespace("Subcontractor", description="Subcontractor namespace")
