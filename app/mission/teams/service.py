import os

from flask import request
from flask_sqlalchemy import Pagination
from sqlalchemy import or_
from sqlalchemy.orm import query

import app.mission.missions.service as mission_service
import app.admin.agencies.service as agency_service
import app.admin.antennas.service as antenna_service
import app.auth.users.service as user_service

from app import db
from app.auth.users import User
from app.auth.users.model import UserRole
from app.common.exceptions import InconsistentUpdateIdException
from app.common.search import sort_query
from app.common.tasks import create_task
from app.mission.missions.service import MISSION_INIT_QUEUE_NAME
from app.mission.teams.error_handlers import TeamNotFoundException
from app.mission.teams import Team
from app.mission.teams.interface import TeamInterface, TeamListInterface
from app.mission.teams.model import UserTeamPositions

TEAMS_DEFAULT_PAGE = 1
TEAMS_DEFAULT_PAGE_SIZE = 100
TEAMS_DEFAULT_SORT_FIELD = "id"
TEAMS_DEFAULT_SORT_DIRECTION = "desc"

MISSION_MANAGERS_DEFAULT_PAGE = 1
MISSION_MANAGERS_DEFAULT_PAGE_SIZE = 20
MISSION_MANAGERS_DEFAULT_SORT_FIELD = "id"
MISSION_MANAGERS_DEFAULT_SORT_DIRECTION = "desc"


class TeamService:
    @staticmethod
    def get_all(mission_id=None):
        q = sort_query(Team.query)
        if mission_id is not None:
            q = q.filter(Team.mission_id == mission_id)

        teams = q.all()

        team_list = {
            "mission_managers": [],
            "collaborators": [],
            "external_collaborators": [],
            "users_additional_access": [],
            "agencies_additional_access": [],
            "antennas_additional_access": [],
            "client_access": [],
        }

        for team in teams:
            if team.user_id and team.user_position == UserTeamPositions.MISSION_MANAGER:
                team_list["mission_managers"].append(team.user)
            elif team.user_id and team.user_position == UserTeamPositions.COLLABORATOR:
                team_list["collaborators"].append(team.user)
            elif (
                team.user_id
                and team.user_position == UserTeamPositions.EXTERNAL_COLLABORATOR
            ):
                team_list["external_collaborators"].append(team.user)
            elif team.user_id and team.user_position == UserTeamPositions.CLIENT_ACCESS:
                team_list["client_access"].append(team.user)
            elif (
                team.user_id
                and team.user_position == UserTeamPositions.ADDITIONAL_ACCESS
            ):
                team_list["users_additional_access"].append(team.user)
            elif team.agency_id:
                team_list["agencies_additional_access"].append(team.agency)
            elif team.antenna_id:
                team_list["antennas_additional_access"].append(team.antenna)

        return team_list

    @staticmethod
    def get_all_mission_managers(
        page=MISSION_MANAGERS_DEFAULT_PAGE,
        size=MISSION_MANAGERS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=MISSION_MANAGERS_DEFAULT_SORT_FIELD,
        direction=MISSION_MANAGERS_DEFAULT_SORT_DIRECTION,
        mission_id=None
    ) -> Pagination:
        q = User.query.join(Team, Team.user_id == User.id)
        q = q.filter(Team.user_position == UserTeamPositions.MISSION_MANAGER).distinct(
            User.id
        )
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                )
            )
        if mission_id:
            q = q.filter(Team.mission_id == mission_id)
        q = sort_query(q, sort_by, direction)
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(team_id: str) -> Team:
        db_team = Team.query.get(team_id)
        if db_team is None:
            raise TeamNotFoundException
        return db_team

    @staticmethod
    def create(new_attrs: TeamInterface) -> Team:
        """Create a new team in a given agency"""
        mission_service.MissionService.get_by_id(new_attrs.get("mission_id"))

        if new_attrs.get("user_id"):
            user_service.UserService.get_by_id(new_attrs.get("user_id"))
        elif new_attrs.get("agency_id"):
            agency_service.AgencyService.get_by_id(new_attrs.get("agency_id"))
        elif new_attrs.get("antenna_id"):
            antenna_service.AntennaService.get_by_id(new_attrs.get("antenna_id"))

        team = Team(**new_attrs)
        db.session.add(team)
        db.session.commit()
        return team

    @staticmethod
    def create_list(new_attrs: TeamListInterface, update=True, user=None):
        # Create our teams
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.MISSION_MANAGER,
                    mission_id=new_attrs.get("mission_id"),
                    user_id=user.get("id"),
                )
            )
            for user in new_attrs.get("mission_managers")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.COLLABORATOR,
                    mission_id=new_attrs.get("mission_id"),
                    user_id=user.get("id"),
                )
            )
            for user in new_attrs.get("collaborators")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.EXTERNAL_COLLABORATOR,
                    mission_id=new_attrs.get("mission_id"),
                    user_id=user.get("id"),
                )
            )
            for user in new_attrs.get("external_collaborators")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.ADDITIONAL_ACCESS,
                    mission_id=new_attrs.get("mission_id"),
                    user_id=user.get("id"),
                )
            )
            for user in new_attrs.get("users_additional_access")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.ADDITIONAL_ACCESS,
                    mission_id=new_attrs.get("mission_id"),
                    agency_id=agency.get("id"),
                )
            )
            for agency in new_attrs.get("agencies_additional_access")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.ADDITIONAL_ACCESS,
                    mission_id=new_attrs.get("mission_id"),
                    antenna_id=antenna.get("id"),
                )
            )
            for antenna in new_attrs.get("antennas_additional_access")
        ]
        [
            TeamService.create(
                TeamInterface(
                    user_position=UserTeamPositions.CLIENT_ACCESS,
                    mission_id=new_attrs.get("mission_id"),
                    user_id=user.get("id"),
                )
            )
            for user in new_attrs.get("client_access")
        ]

        if user is not None and (user.role in [UserRole.MANAGER, UserRole.ADMIN]):
            exists = Team.query.filter(
                Team.user_id == user.id, Team.mission_id == new_attrs.get("mission_id")
            ).first()
            if not exists:
                TeamService.create(
                    TeamInterface(
                        user_position=UserTeamPositions.ADDITIONAL_ACCESS,
                        mission_id=new_attrs.get("mission_id"),
                        user_id=user.id,
                    )
                )

        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=MISSION_INIT_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/missions/compute-permissions",
            method="POST",
            payload={"mission_id": new_attrs.get("mission_id"), "update": update},
        )

    @staticmethod
    def update(team: Team, changes: TeamInterface, force_update: bool = False) -> Team:
        if force_update or TeamService.has_changed(team, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != team.id:
                raise InconsistentUpdateIdException
            team.update(changes)
            db.session.commit()
        return team

    @staticmethod
    def update_list(new_attrs: TeamListInterface):
        # Delete previous teams for the mission
        old_teams = Team.query.filter_by(mission_id=new_attrs.get("mission_id")).all()
        [TeamService.delete_by_id(team.id) for team in old_teams]

        # Create new team list for the mission
        TeamService.create_list(new_attrs)

    @staticmethod
    def has_changed(team: Team, changes: TeamInterface) -> bool:
        for key, value in changes.items():
            if getattr(team, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(team_id: int) -> int or None:
        team = Team.query.filter(Team.id == team_id).first()
        if not team:
            raise TeamNotFoundException
        db.session.delete(team)
        db.session.commit()
        return team_id
