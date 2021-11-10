from app.common.api import AuthenticatedApi
from . import api
from flask_accepts import responds
from .service import JobService


@api.route("")
class JobResource(AuthenticatedApi):
    # @responds(many=True, api=api)
    def get(self):
        return JobService.get_all()
