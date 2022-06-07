from operator import or_
from typing import List

from flask_sqlalchemy import Pagination

from app import db
from app.auth.users import User
from app.common.search import sort_query
from app.project.project_leads.error_handlers import (
    ProjectLeadNotFoundException,
    UnidentifiedReferrerException,
)
from app.project.project_leads.interface import ProjectLeadInterface
from app.project.project_leads.model import ProjectLead
import app.project.projects.service as project_service
import app.auth.users.service as user_service

REFERRERS_DEFAULT_PAGE = 1
REFERRERS_DEFAULT_PAGE_SIZE = 20
REFERRERS_DEFAULT_SORT_FIELD = "id"
REFERRERS_DEFAULT_SORT_DIRECTION = "desc"


class ProjectLeadService:
    @staticmethod
    def create(new_attrs: ProjectLeadInterface) -> ProjectLead:
        """Create a new project_lead for a project"""

        # Check if project exists
        project_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        # Check if user exists
        user_service.UserService.get_by_id(new_attrs.get("user_id"))

        project_lead = ProjectLead(**new_attrs)
        db.session.add(project_lead)
        db.session.commit()
        return project_lead.user

    @staticmethod
    def get_all(
        page=REFERRERS_DEFAULT_PAGE,
        size=REFERRERS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=REFERRERS_DEFAULT_SORT_FIELD,
        direction=REFERRERS_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        """Get all referrers"""
        q = User.query.join(User.project_leads)
        q = sort_query(q, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                )
            )
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create_list(project_id: int, new_attrs: List):
        # Create our project_leads
        users = []
        for user in new_attrs:
            if "id" not in user:
                raise UnidentifiedReferrerException
            users.append(
                ProjectLeadService.create(
                    ProjectLeadInterface(project_id=project_id, user_id=user.get("id"))
                )
            )
        return users

    @staticmethod
    def get_by_id(project_lead_id: str) -> ProjectLead:
        db_project_lead = ProjectLead.query.get(project_lead_id)
        if db_project_lead is None:
            raise ProjectLeadNotFoundException
        return db_project_lead

    @staticmethod
    def get_by_user_and_project(user_id: str, project_id) -> ProjectLead:
        db_project_lead = ProjectLead.query.filter(
            ProjectLead.mission_id == project_id, ProjectLead.user_id == user_id
        ).first()
        if db_project_lead is None:
            raise ProjectLeadNotFoundException
        return db_project_lead

    @staticmethod
    def update_list(referrers: dict, project_id: int):
        # Get previous project_leads for the project
        old_project_leads = ProjectLead.query.filter_by(project_id=project_id).all()
        referrers_existing_id = [
            project_lead.user_id for project_lead in old_project_leads
        ]

        for referrer in referrers:
            # If referrer does not have an id, it does not exist and should not be added as project_lead
            if "id" not in referrer:
                raise UnidentifiedReferrerException()
            # If referrer is already linked to the project,
            # nothing must be done (because referrer's update would be instead a user update).
            # Else, it's added as new project_lead
            if "id" in referrer and referrer["id"] not in referrers_existing_id:
                # Check if referrer exists as a user into db
                user_service.UserService.get_by_id(referrer.get("id"))

                ProjectLeadService.create(
                    ProjectLeadInterface(
                        project_id=project_id, user_id=referrer.get("id")
                    )
                )
        # Compare old project_leads list and new referrers. Remove obsolete project_leads
        for old_project_lead in old_project_leads:
            is_removed = True
            for referrer in referrers:
                if "id" in referrer and referrer["id"] == old_project_lead.user_id:
                    is_removed = False
                    break
            if is_removed:
                ProjectLeadService.delete_by_id(old_project_lead.id)

    @staticmethod
    def delete_by_id(project_lead_id: int) -> int or None:
        project_lead = ProjectLead.query.filter(
            ProjectLead.id == project_lead_id
        ).first()
        if not project_lead:
            raise ProjectLeadNotFoundException
        db.session.delete(project_lead)
        db.session.commit()
        return project_lead_id
