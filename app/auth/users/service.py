import os
from typing import List
from urllib.parse import urlencode

from flask_sqlalchemy import Pagination
from googleapiclient.errors import HttpError
from sqlalchemy import or_, and_
from flask import g
import logging

from .error_handlers import UserNotFoundException, UnknownConnexionEmail, InactiveUser
from .interface import UserInterface
from .model import User, UserKind, UserRole, UserGroup
from app import db
from ..preferred_app import PreferredApp
from ...admin.agencies import Agency
from ...admin.antennas import Antenna
from ...common import Permission, Role
from app.auth.error_handlers import InvalidSearchFieldException
from ...common.app_name import App
from ...common.google_apis import DirectoryService, CloudIdentityService
from ...common.group_utils import GroupUtils
from ...common.identity_utils import IdentityUtils
from ...common.search import sort_query
from ...mission.missions import Mission
from ...mission.missions.exceptions import MissionNotFoundException
from ...mission.teams import Team

USERS_DEFAULT_PAGE = 1
USERS_DEFAULT_PAGE_SIZE = 20
USERS_DEFAULT_SORT_FIELD = "email"
USERS_DEFAULT_SORT_DIRECTION = "asc"


class UserService:
    @staticmethod
    def get_all(
        page=USERS_DEFAULT_PAGE,
        size=USERS_DEFAULT_PAGE_SIZE,
        kind=None,
        term=None,
        sort_by=USERS_DEFAULT_SORT_FIELD,
        direction=USERS_DEFAULT_SORT_DIRECTION,
        role=None,
        no_clients=False,
    ) -> Pagination:
        q = sort_query(User.query, sort_by, direction)
        if kind:
            q = q.filter(User.kind == kind)
        if term:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.role.ilike(search_term),
                    User.kind.ilike(search_term),
                    User.groups.any(
                        UserGroup.agency.has(Agency.name.ilike(search_term))
                    ),
                    User.groups.any(
                        UserGroup.antenna.has(Antenna.name.ilike(search_term))
                    ),
                )
            )

            # Filter by role
            if role is not None and role not in [
                "admin",
                "manager",
                "contributor",
                "client",
            ]:
                raise InvalidSearchFieldException()
            if role is not None:
                q = q.filter(User.role == role)
            if no_clients is True:
                q = q.filter(User.role != "client")

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: UserInterface) -> User:
        if new_attrs.get("kind") == UserKind.OTHER:
            new_attrs = UserService.signup_new_user(new_attrs)

        preferred_app = PreferredApp(
            **{"preferred_app": App.INDIVIDUAL, "first_connection": True}
        )

        db.session.add(preferred_app)
        db.session.commit()

        new_user = User(**new_attrs)
        new_user.preferred_app_id = preferred_app.id
        db.session.add(new_user)

        db.session.commit()

        if new_user.role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.CONTRIBUTOR]:
            if not GroupUtils.is_member_of(
                new_user.email, os.getenv("APPLICATION_MEMBERS_GOOGLE_GROUP")
            ):
                GroupUtils.add_member(
                    new_user.email, os.getenv("APPLICATION_MEMBERS_GOOGLE_GROUP")
                )

        if new_user.role == UserRole.ADMIN:
            if not GroupUtils.is_member_of(
                new_user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
            ):
                GroupUtils.add_member(
                    new_user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
                )

        return new_user

    @staticmethod
    def signup_new_user(user_attrs):
        # Return user_attrs with UID
        user_attrs["uid"] = IdentityUtils.create_user(user_attrs)
        IdentityUtils.send_reset_password_email(user_attrs["email"])
        return user_attrs

    @staticmethod
    def get_by_id(user_id: int) -> User:
        db_user = User.query.get(user_id)
        if not db_user:
            raise UserNotFoundException
        return db_user

    @staticmethod
    def get_by_email(user_email: str) -> User:
        return User.query.filter_by(email=user_email).first()

    @staticmethod
    def update(user: User, changes: UserInterface, force_update: bool = False) -> User:
        if force_update or UserService.has_changed(user, changes):
            old_user_role = user.role
            user.update(changes)
            db.session.commit()
            if user.role == UserRole.ADMIN and old_user_role != UserRole.ADMIN:
                if not GroupUtils.is_member_of(
                    user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
                ):
                    GroupUtils.add_member(
                        user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
                    )
            elif user.role != UserRole.ADMIN and old_user_role == UserRole.ADMIN:
                if GroupUtils.is_member_of(
                    user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
                ):
                    GroupUtils.remove_member(
                        user.email, os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP")
                    )
        return user

    @staticmethod
    def check_auth_informations(
        email: str, changes: UserInterface, force_update: bool = False
    ) -> User:
        """
        A user connecting to the app is always already registered.
        Because the admin creates all users before they sign in for the
        first time.
        Email is used as a the check field. If email does not already exist
        into db, it's a forbidden connexion attempt.
        """
        db_user = UserService.get_by_email(email)
        if not db_user:
            google_info = UserService.get_user_info_from_gsuite(email)
            if not google_info:
                raise UnknownConnexionEmail
            else:
                db_user = UserService.create(
                    UserInterface(
                        uid=changes.get("uid"),
                        email=email,
                        last_name=google_info.get("name", {}).get("familyName"),
                        first_name=google_info.get("name", {}).get("givenName"),
                        kind=UserKind.EMPLOYEE,
                        active=False,
                        role=UserRole.CONTRIBUTOR,
                    )
                )
        if db_user.active is False:
            raise InactiveUser
        return UserService.update(db_user, changes, force_update)

    @staticmethod
    def has_changed(user: User, changes: UserInterface) -> bool:
        for key, value in changes.items():
            if getattr(user, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(user_id: int) -> int or None:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException

        if GroupUtils.is_member_of(
            user.email, os.getenv("APPLICATION_MEMBERS_GOOGLE_GROUP")
        ):
            GroupUtils.remove_member(
                user.email, os.getenv("APPLICATION_MEMBERS_GOOGLE_GROUP")
            )

        if user.uid is not None:
            IdentityUtils.delete_user(user.uid)
        db.session.delete(user)
        PreferredApp.query.filter_by(id=user.preferred_app_id).delete()
        db.session.commit()
        return user_id

    @staticmethod
    def get_user_info_from_gsuite(email: str) -> dict or None:
        client = DirectoryService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()
        try:
            response = (
                client.users()
                .get(userKey=email, fields="primaryEmail,name")
                .execute(num_retries=3)
            )
            return response
        except HttpError as e:
            logging.error(f"Unable to retrieve user {email} from GSuite: {e}")
        return None

    @staticmethod
    def get_user_groups_from_gsuite(email: str) -> [str] or None:
        client = CloudIdentityService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()
        groups = []
        error = False
        params = {
            "query": f"member_key_id == '{email}' && 'cloudidentity.googleapis.com/groups.discussion_forum' in labels",
            "page_size": 50,
        }
        while True:
            query_params = urlencode(params)
            try:
                request = (
                    client.groups()
                    .memberships()
                    .searchTransitiveGroups(parent="groups/-")
                )
                request.uri += "&" + query_params
                response = request.execute(num_retries=3)

                for membership in response.get("memberships", []):
                    if "groupKey" in membership:
                        groups.append(membership["groupKey"].get("id"))

                if response.get("nextPageToken"):
                    params["pageToken"] = response.get("nextPageToken")
                else:
                    break
            except HttpError as e:
                logging.error(
                    f"Unable to retrieve user {email} groups from Google Workspace: {e}"
                )
                error = True
                break
        if error:
            dclient = DirectoryService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()
            groups = []
            params = dict(userKey=email, fields="nextPageToken,groups(email)")
            while True:
                try:
                    response = dclient.groups().list(**params).execute(num_retries=3)
                    groups.extend(
                        [group.get("email") for group in response.get("groups", [])]
                    )
                    if response.get("nextPageToken"):
                        params["pageToken"] = response.get("nextPageToken")
                    else:
                        break
                except HttpError as e:
                    logging.error(
                        f"Unable to retrieve user {email} groups from GSuite: {e}"
                    )
                    return None

        return groups

    @staticmethod
    def update_user_groups(user: User):
        source_groups = UserService.get_user_groups_from_gsuite(user.email)
        if source_groups is not None:
            agencies = Agency.query.filter(
                Agency.email_address.in_(source_groups)
            ).all()
            antennas = Antenna.query.filter(
                Antenna.email_address.in_(source_groups)
            ).all()

            agencies_data = {}
            for agency in agencies:
                agencies_data[agency.email_address] = agency
            antennas_data = {}
            for antenna in antennas:
                antennas_data[antenna.email_address] = antenna
                if (
                    antenna.agency
                    and antenna.agency.email_address
                    and antenna.agency.email_address not in agencies_data
                ):
                    agencies_data[antenna.agency.email_address] = antenna.agency

            if agencies_data or antennas_data:
                existing_groups = UserGroup.query.filter(UserGroup.user == user).all()
                existing_groups_emails = [
                    group.group_email for group in existing_groups
                ]
                groups_to_delete = []
                for existing_group in existing_groups:
                    if (
                        existing_group.group_email not in agencies_data.keys()
                        and existing_group.group_email not in antennas_data.keys()
                    ):
                        groups_to_delete.append(existing_group)

                groups_to_add = []
                for email, agency in agencies_data.items():
                    if email not in existing_groups_emails:
                        groups_to_add.append(
                            UserGroup(user=user, group_email=email, agency=agency)
                        )

                for email, antenna in antennas_data.items():
                    if email not in existing_groups_emails:
                        groups_to_add.append(
                            UserGroup(user=user, group_email=email, antenna=antenna)
                        )

                for group_to_delete in groups_to_delete:
                    db.session.delete(group_to_delete)
                for group_to_add in groups_to_add:
                    db.session.add(group_to_add)
            else:
                db.session.query(UserGroup).filter(UserGroup.user == user).delete()

            db.session.commit()

    def get_users_list(id_list: List[int]) -> List[User]:
        # Retrieve a list of user objects from a list of ids
        users = User.query.filter(User.id.in_(id_list)).all()
        if len(users) != len(id_list):
            raise UserNotFoundException
        return users

    @staticmethod
    def get_permissions_for_role(role: Role) -> List:
        permissions = Permission.query.filter(
            Permission.role.has(Role.value >= role.value)
        ).all()
        output = {}
        for p in permissions:
            if p.entity not in output:
                output[p.entity] = []
            output[p.entity].append(p.action)

        return [dict(subject=k, actions=v) for k, v in output.items()]

    @staticmethod
    def list_users_by_mission_id(mission_id: int, term: str):
        mission = Mission.query.get(mission_id)
        if not mission:
            raise MissionNotFoundException
        users_query = (
            User.query.join(Team)
            .join(UserGroup, isouter=True)
            .filter(
                or_(
                    Team.mission_id == mission_id,
                    UserGroup.agency_id == mission.agency_id,
                    UserGroup.antenna_id == mission.antenna_id,
                )
            )
        )
        if term:
            term = f"%{term}%"
            users_query = users_query.filter(User.email.ilike(term))
        return users_query.all()
