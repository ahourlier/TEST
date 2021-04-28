from .model import Requester

from flask_restx import Namespace

# from .schema import RequesterSchema

api = Namespace("Requesters", description="Requesters namespace")
