from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from .model import Team
from ...common.schemas import PaginatedSchema
from ...auth.users.schema import UserSchema
from ...admin.agencies.schema import AgencySchema
from ...admin.antennas.schema import AntennaSchema


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True


class TeamSchemaUser(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema())

    class Meta:
        model = Team
        include_fk = True


class TeamPaginatedSchema(PaginatedSchema):
    items = fields.Nested(TeamSchemaUser, many=True, dump_only=True)


class TeamMultipleSchema(Schema):
    mission_id = fields.Integer()
    mission_managers = fields.List(fields.Nested(UserSchema()))
    collaborators = fields.List(fields.Nested(UserSchema()))
    external_collaborators = fields.List(fields.Nested(UserSchema()))
    agencies_additional_access = fields.List(fields.Nested(AgencySchema()))
    antennas_additional_access = fields.List(fields.Nested(AntennaSchema()))
    users_additional_access = fields.List(fields.Nested(UserSchema()))
    client_access = fields.List(fields.Nested(UserSchema()))
