from .model import Project

from flask_restx import Namespace

# try:
#     from .schema import ProjectSchema
# except ImportError:
#     pass

api = Namespace("Projects", description="Projects namespace")
