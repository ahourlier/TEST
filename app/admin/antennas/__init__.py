from flask_restx import Namespace

from .model import Antenna
from .schema import AntennaSchema

api = Namespace("Antennas", description="Antennas namespace")
