from app.common.api import AuthenticatedApi
from .. import api
from .service import JobService


@api.route("/jobs")
class JobResource(AuthenticatedApi):

    # @responds(schema=[JobSchema()], api=api)
    def get(self):
        return JobService.get_all()

