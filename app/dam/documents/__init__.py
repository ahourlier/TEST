from .model import Document

from flask_restx import Namespace

from .schema import DocumentSchema

api = Namespace("Documents", description="Documents namespace")
