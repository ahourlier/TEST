import logging
from flask import g, request, Response, jsonify
from flask_accepts import responds, accepts
from flask_allows import requires
from flask_restx import inputs
from flask_sqlalchemy import Pagination
import gc
import psutil
import os

from . import api
from .interface import UserInterface
from .schema import (
    UserSchema,
    UserPaginatedSchema,
    UserAuthSchema,
    UserLightSchema,
    UsersInItemsSchema,
)
from .model import User, UserRole
from .service import (
    UserService,
    USERS_DEFAULT_PAGE,
    USERS_DEFAULT_PAGE_SIZE,
    USERS_DEFAULT_SORT_FIELD,
    USERS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import is_admin
from ...common.search import SEARCH_PARAMS


@api.route("/me")
class UserMe(AuthenticatedApi):
    """ Current user profile """

    @responds(schema=UserAuthSchema)
    def get(self):
        gc.collect()
        process = psutil.Process(os.getpid())
        print(f"first process memory in bytes: {process.memory_info().rss}")  # in bytes
        UserService.update_user_groups(g.user)
        print("updated user groups")
        permissions = UserService.get_permissions_for_role(g.user.role_data)
        print("finished fetching permissions")
        setattr(g.user, "permissions", permissions)
        gc.collect()
        process = psutil.Process(os.getpid())
        print(f"second process memory in bytes: {process.memory_info().rss}")  # in bytes
        return g.user


@api.route("/")
class UsersResource(AuthenticatedApi):
    """ users/collaborators api """

    @accepts(
        *SEARCH_PARAMS,
        dict(name="kind", type=str),
        dict(name="role", type=str),
        dict(name="no_clients", type=inputs.boolean),
        api=api,
    )
    @responds(schema=UserPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all users """
        return UserService.get_all(
            page=int(request.args.get("page", USERS_DEFAULT_PAGE)),
            size=int(request.args.get("size", USERS_DEFAULT_PAGE_SIZE)),
            kind=request.args.get("kind"),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", USERS_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", USERS_DEFAULT_SORT_DIRECTION),
            role=str(request.args.get("role"))
            if request.args.get("role") not in [None, ""]
            else None,
            no_clients=True if request.args.get("no_clients") == "True" else False,
        )

    @accepts(schema=UserSchema, api=api)
    @responds(schema=UserSchema)
    @requires(is_admin)
    def post(self) -> User:
        """ Create an user """
        return UserService.create(request.parsed_obj)


@api.route("/<int:user_id>")
@api.param("userId", "User unique ID")
class UserIdResource(AuthenticatedApi):
    @responds(schema=UserSchema)
    def get(self, user_id: int) -> User:
        """ Get single user """

        return UserService.get_by_id(user_id)

    @requires(is_admin)
    def delete(self, user_id: int) -> Response:
        """Delete single user"""

        id = UserService.delete_by_id(user_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=UserSchema, api=api)
    @responds(schema=UserSchema)
    @requires(is_admin)
    def put(self, user_id: int) -> User:
        """Update single user"""

        changes: UserInterface = request.parsed_obj
        db_user = UserService.get_by_id(user_id)
        return UserService.update(db_user, changes)


@api.route("/mission/<int:mission_id>")
@api.param("missionId", "Mission unique ID")
class UserByMissionResource(AuthenticatedApi):
    @responds(schema=UsersInItemsSchema())
    @accepts(
        dict(name="term", type=str), api=api,
    )
    def get(self, mission_id: int):
        return UserService.list_users_by_mission_id(
            mission_id, term=request.args.get("term"),
        )
