from flask_restx import Resource

from app.common.decorators import auth_required


class AuthenticatedApi(Resource):
    """Base class for authenticated apis"""

    decorators = [auth_required]
