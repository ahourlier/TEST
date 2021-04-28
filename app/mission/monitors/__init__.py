from flask_restx import Namespace

from .model import Monitor

api = Namespace("Monitoring", description="Mission funders monitor Namespace")
