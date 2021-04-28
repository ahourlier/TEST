from .model import CommonArea

from flask_restx import Namespace

from .schema import CommonAreaSchema

api = Namespace("CommonAreas", description="CommonAreas namespace")
