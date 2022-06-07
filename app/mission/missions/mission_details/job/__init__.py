from .model import Job
from .schema import JobSchema
from flask_restx import Namespace


api = Namespace("Job", description="Job namespace")
