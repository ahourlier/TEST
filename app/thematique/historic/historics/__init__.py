from flask_restx import Namespace
from .model import Historic
from .schema import HistoricSchema


api = Namespace("Historics", description="Historic namespace")
