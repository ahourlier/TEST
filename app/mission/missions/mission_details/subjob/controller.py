from app.common.api import AuthenticatedApi
from .service import SubjobService
from .. import api


@api.route("/subjobs")
class SubjobsResource(AuthenticatedApi):

    # @responds(schema=[JobSchema()], api=api)
    def get(self):
        return SubjobService.get_all()

