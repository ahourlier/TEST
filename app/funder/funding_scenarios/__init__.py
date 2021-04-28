from flask_restx import Namespace
from .model import FundingScenario
from .schema import FundingScenarioSchema


api = Namespace("Funding Scenarios", description="Funding Scenarios namespace")
