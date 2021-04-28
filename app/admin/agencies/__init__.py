from flask_restx import Namespace

from .model import Agency
from .schema import AgencySchema

api = Namespace("Agencies", description="Agencies namespace")
