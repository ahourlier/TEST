from .model import PreferredApp

from flask_restx import Namespace
from .schema import PreferredAppSchema

api = Namespace("PreferredApp", description="Preferred app namespace")
