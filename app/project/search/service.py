import json
from typing import List

from flask import g
from flask_sqlalchemy import Pagination
from psycopg2.extensions import JSON
from sqlalchemy.sql.elements import or_, and_

from app import db
from app.auth.users.model import UserRole
from app.common.exceptions import InconsistentUpdateIdException, ForbiddenException
from app.mission.missions import Mission
from app.mission.teams import Team
from app.mission.teams.model import UserTeamPositions
from app.project.project_custom_fields.model import ProjectCustomField
from app.project.projects import Project
from app.project.requesters import Requester

from app.project.search.error_handlers import SearchNotFoundException
from app.project.search.interface import SearchInterface
from app.project.search.model import Search
from app.common.search import SearchService, sort_query

SEARCH_DEFAULT_PAGE = 1
SEARCH_DEFAULT_PAGE_SIZE = 20
SEARCH_DEFAULT_SORT_FIELD = "id"
SEARCH_DEFAULT_SORT_DIRECTION = "desc"

SAVED_SEARCH_DEFAULT_PAGE = 1
SAVED_SEARCH_DEFAULT_PAGE_SIZE = 5
SAVED_SEARCH_DEFAULT_SORT_FIELD = "id"
SAVED_SEARCH_DEFAULT_SORT_DIRECTION = "desc"


SEARCH_TERM_DEFAULT_FIELDS = [
    "code_name",
    "requester.first_name",
    "requester.last_name",
]
MANAGER_FILTER = "mission_manager"


class ProjectSearchService:
    @staticmethod
    def search_projects(
        search: JSON,
        page=SEARCH_DEFAULT_PAGE,
        size=SEARCH_DEFAULT_PAGE_SIZE,
        sort_by=SEARCH_DEFAULT_SORT_FIELD,
        direction=SEARCH_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        """Extract specific project case : MANAGERS """
        manager_filter = None
        custom_fields = []
        for f in search["filters"]:
            try:
                # check if field is a custom field
                custom_field_id = int(f.get("field"))
                custom_fields.append(
                    {"custom_field_id": custom_field_id, "values": f.get("values")}
                )
                search["filters"].remove(f)
            except ValueError:
                # not a custom field
                pass
            if f["field"] == MANAGER_FILTER:
                manager_filter = f
                search["filters"].remove(f)
        q = SearchService.search_into_model(Project, search, SEARCH_TERM_DEFAULT_FIELDS)
        # Filter specificaly on managers :
        if manager_filter:
            q = ProjectSearchService.filter_on_managers(q, manager_filter)

        # Filter on custom fields
        if len(custom_fields) > 0:
            q = ProjectSearchService.filter_on_custom_fields(q, custom_fields)

        # Deactivated projects must not be retrieved
        q = q.filter(Project.active == True)
        # Filter query on current user access
        q = ProjectSearchService.check_user_project_access(q)

        if sort_by == "requester_last_name":
            q = q.join(Project.requester).order_by(
                Requester.last_name.asc()
                if direction == "asc"
                else Requester.last_name.desc()
            )
        else:
            q = sort_query(q, sort_by, direction)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def filter_on_managers(q, manager_filter):
        values = manager_filter["values"]
        # As targetted values, we may receive a list of IDs OR plain dicts from the front-app.
        # If plain dicts, we need here to flatten values by extracting their ids
        for i, value in enumerate(values):
            if isinstance(value, dict):
                values[i] = value["id"]

        q = q.filter(
            Project.mission.has(
                Mission.teams.any(
                    and_(
                        Team.user_position == UserTeamPositions.MISSION_MANAGER,
                        or_(
                            *[
                                Team.user_id == value
                                for value in values
                                if value is not None
                            ]
                        ),
                    )
                )
            )
        )
        return q

    @staticmethod
    def filter_on_custom_fields(q, custom_fields):
        q = q.join(ProjectCustomField)
        for c in custom_fields:
            q = q.filter(
                and_(
                    ProjectCustomField.custom_field_id == c.get("custom_field_id"),
                    *[
                        ProjectCustomField.value.ilike(f"%{v}%")
                        for v in c.get("values")
                    ],
                )
            )
        return q

    @staticmethod
    def check_user_project_access(q):
        """Limit search results for projects with only accessibles projects for the current user"""
        user = g.user
        if not user.role == UserRole.ADMIN:
            user_agencies = [
                group.agency_id for group in user.groups if group.agency_id
            ]
            user_antennas = [
                group.antenna_id for group in user.groups if group.antenna_id
            ]
            q = q.join(Mission).filter(
                Mission.teams.any(
                    or_(
                        Team.user_id == user.id,
                        Team.antenna_id.in_(user_antennas),
                        Team.agency_id.in_(user_agencies),
                    )
                )
            )
        return q


class ProjectRegisterSearchService:
    @staticmethod
    def create(new_attrs: SearchInterface) -> Search:
        new_attrs["user_id"] = g.user.id
        new_attrs["search"] = json.dumps(new_attrs["search"])
        new_search = Search(**new_attrs)
        db.session.add(new_search)
        db.session.commit()
        return new_search

    @staticmethod
    def get_all_raw() -> List[Search]:
        db_search = Search.query.filter(Search.user_id == g.user.id).all()
        return db_search

    @staticmethod
    def get_all_paginated(
        page=SAVED_SEARCH_DEFAULT_PAGE,
        size=SAVED_SEARCH_DEFAULT_PAGE_SIZE,
        sort_by=SAVED_SEARCH_DEFAULT_SORT_FIELD,
        direction=SAVED_SEARCH_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        base_q = sort_query(Search.query, sort_by, direction)
        q = base_q.filter(Search.user_id == g.user.id)
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(search_id: str) -> Search:
        db_search = Search.query.get(search_id)
        if db_search is None:
            raise SearchNotFoundException
        if db_search.user_id is not g.user.id:
            raise ForbiddenException()
        return db_search

    @staticmethod
    def update(
        search: Search, changes: SearchInterface, force_update: bool = False
    ) -> Search:
        if force_update or ProjectSearchService.has_changed(search, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != search.id:
                raise InconsistentUpdateIdException()
            search.update(changes)
            db.session.commit()
        return search

    @staticmethod
    def has_changed(search: Search, changes: SearchInterface) -> bool:
        for key, value in changes.items():
            if getattr(search, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(search_id: int) -> List[Search]:
        search = Search.query.filter(Search.id == search_id).first()
        if not search:
            raise SearchNotFoundException
        if search.user_id is not g.user.id:
            raise ForbiddenException()
        db.session.delete(search)
        db.session.commit()
        return ProjectRegisterSearchService.get_all()
