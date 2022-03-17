import functools
import os

import google.auth.transport.requests
import google.oauth2.id_token

from flask import request, g, jsonify

from app.auth.users.interface import UserInterface
from app.auth.users.service import UserService

HTTP_REQUEST = google.auth.transport.requests.Request()


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db_user = None
        if "Authorization" in request.headers:
            id_token = request.headers["Authorization"].split(" ").pop()
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, HTTP_REQUEST
            )
            if not claims:  # pragma: no cover
                return "Unauthorized", 401  # TODO raise proper error here

            db_user = UserService.check_auth_informations(
                claims.get("email"),
                UserInterface(
                    **{
                        "uid": claims.get("sub"),
                        "email": claims.get("email"),
                    }
                ),
            )
        else:
            return "Unauthorized", 401
        g.user = db_user
        return func(*args, **kwargs)

    return wrapper
