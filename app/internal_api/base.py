from flask import Blueprint
from flask.views import MethodView


def create_blueprint():
    return Blueprint("Internal API", __name__, url_prefix="/_internal")


internal_api_blueprint = create_blueprint


class InternalAPIView(MethodView):
    decorators = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
