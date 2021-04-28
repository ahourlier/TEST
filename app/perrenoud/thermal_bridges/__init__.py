from flask_restx import Namespace
from .model import ThermalBridge

api = Namespace("ThermalBridges", description="Thermal Bridges namespace")
