from .model import Contact

from flask_restx import Namespace

from .schema import ContactSchema

api = Namespace("Contacts", description="Contacts namespace")
