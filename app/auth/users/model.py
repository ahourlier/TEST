from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin

# Do not remove, used for relationships
from app.admin.agencies import Agency
from app.admin.antennas import Antenna


class UserKind:
    EMPLOYEE = "employee"
    OTHER = "other"


class UserRole:
    ADMIN = "admin"
    MANAGER = "manager"
    CONTRIBUTOR = "contributor"
    CLIENT = "client"


class User(BaseMixin, db.Model):
    """ Application User """

    __tablename__ = "user"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    uid = Column(String(128), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    last_name = Column(String(255), unique=False)
    first_name = Column(String(255), unique=False)
    title = Column(String(10), nullable=True)
    comment = Column(String(2083), nullable=True)
    role = Column(String(255), ForeignKey("role.name"), unique=False)
    preferred_app_id = Column(Integer(), ForeignKey("preferred_app.id"))
    preferred_app = relationship("PreferredApp", cascade="all, delete")
    role_data = relationship("Role", backref="user")
    active = Column(Boolean(create_constraint=False), default=True, nullable=False)
    kind = Column(String(20), default=UserKind.EMPLOYEE, nullable=False)

    @hybrid_property
    def projects_id(self):
        import app.project.permissions as projects_permissions
        from app.project.projects import Project

        q = Project.query
        projects = projects_permissions.ProjectPermission.filter_query_project_by_user_permissions(
            q, user=self
        ).all()
        return [project.id for project in projects]


class UserGroup(BaseMixin, db.Model):
    """ Groups associated to a user """

    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref=backref("groups", cascade="all, delete"))
    group_email = Column(String(255), nullable=False)
    antenna_id = Column(Integer, ForeignKey("antenna.id"), nullable=True)
    antenna = relationship(
        "Antenna", backref=backref("antennas", cascade="all, delete")
    )
    agency_id = Column(Integer, ForeignKey("agency.id"), nullable=True)
    agency = relationship("Agency", backref=backref("agencies", cascade="all, delete"))
