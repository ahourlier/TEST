from app.common.api import AuthenticatedApi
from .schema import SubjobSchema
from .service import SubjobService
from . import api
from flask_accepts import responds


@api.route("")
class SubjobsResource(AuthenticatedApi):
    @responds(schema=SubjobSchema, many=True, api=api)
    def get(self):
        return SubjobService.get_all()
