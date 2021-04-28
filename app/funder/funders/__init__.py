from flask_restx import Namespace
from .model import Funder
from .schema import FunderSchema


api = Namespace("Funders", description="Funders namespace")
