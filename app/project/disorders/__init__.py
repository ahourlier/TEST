from .model import Disorder, DisorderType

from flask_restx import Namespace

from .schema import DisorderSchema

api = Namespace("Disorders", description="Disorders namespace")
