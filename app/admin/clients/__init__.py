from flask_restx import Namespace

from .model import Client

api = Namespace("Clients", description="Clients namespace")
