from .model import Simulation

from flask_restx import Namespace

from .schema import SimulationSchema

api = Namespace("Simulations", description="Simulations namespace")
