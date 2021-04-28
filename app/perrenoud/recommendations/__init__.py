from flask_restx import Namespace
from .model import Recommendation

api = Namespace("Recommendations", description="Recommendations namespace")
