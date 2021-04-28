from flask_restx import Namespace

from .model import FunderMonitoringValue

api = Namespace(
    "FunderMonitoringValue", description="Funders monitoring values Namespace"
)
