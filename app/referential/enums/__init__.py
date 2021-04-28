from flask_restx import Namespace

from .model import AppEnum, PerrenoudEnum

api = Namespace("Enums", description="Enums namespace")
