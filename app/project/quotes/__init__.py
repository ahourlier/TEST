from .model import Quote

from flask_restx import Namespace

from ..simulations.schema import QuoteSchema

api = Namespace("Quotes", description="Quotes namespace")
