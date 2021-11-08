from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE
from marshmallow.fields import String

from . import UserGroup
from .model import User
from ..preferred_app import PreferredAppSchema
from ...admin.agencies import AgencySchema
from ...admin.antennas import AntennaSchema
from ...common.schemas import PaginatedSchema


class UserGroupSchema(SQLAlchemyAutoSchema):
    agency = fields.Nested(AgencySchema, dump_only=True)
    antenna = fields.Nested(AntennaSchema, dump_only=True)

    class Meta:
        model = UserGroup


class UserSchema(SQLAlchemyAutoSchema):
    groups = fields.List(fields.Nested(UserGroupSchema()), dump_only=True)
    # preferred_app = fields.Nested(PreferredAppSchema())

    class Meta:
        model = User
        include_fk = True
        unknown = EXCLUDE


class UserPermissionSchema(Schema):
    actions = fields.List(String)
    subject = fields.String()


class UserAuthSchema(SQLAlchemyAutoSchema):
    groups = fields.List(fields.Nested(UserGroupSchema()), dump_only=True)
    permissions = fields.List(fields.Nested(UserPermissionSchema), dump_only=True)
    projects_id = fields.List(fields.Integer, dump_only=True)
    preferred_app = fields.Nested(PreferredAppSchema())

    class Meta:
        model = User
        include_fk = True
        unknown = EXCLUDE


class UserPaginatedSchema(PaginatedSchema):
    items = fields.Nested(UserSchema, many=True, dump_only=True)
