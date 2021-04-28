from flask_restx import Namespace

from .model import CustomField

api = Namespace("CustomFields", description="Custom Fields Namespace")
