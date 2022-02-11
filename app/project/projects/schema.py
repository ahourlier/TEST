from flask_marshmallow.sqla import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow import INCLUDE, fields, EXCLUDE, Schema
from marshmallow.fields import Integer

from app.auth.users import UserSchema
from app.common.schemas import PaginatedSchema, DocumentSchema
from app.mission.missions import MissionSchema

from app.project.accommodations.schema import AccommodationSchema
from app.project.common_areas import CommonAreaSchema
from app.project.projects.model import Project

from app.project.requesters.schema import RequesterSchema
from app.project.work_types.schema import WorkTypeSchema


class SectionsPermissionsSchema(Schema):
    ca_requester = fields.Boolean(dump_only=True)
    ca_accommodation = fields.Boolean(dump_only=True)
    ca_common_area = fields.Boolean(dump_only=True)
    ca_accommodation_summary = fields.Boolean(dump_only=True)
    ca_quotes = fields.Boolean(dump_only=True)
    ca_simulations = fields.Boolean(dump_only=True)
    ca_deposit = fields.Boolean(dump_only=True)
    ca_certification = fields.Boolean(dump_only=True)
    ca_payment_request = fields.Boolean(dump_only=True)
    ca_funders = fields.Boolean(dump_only=True)
    ca_documents = fields.Boolean(dump_only=True)
    ca_follow_up = fields.Boolean(dump_only=True)


class ProjectSchema(SQLAlchemyAutoSchema):
    mission = fields.Nested(MissionSchema())
    referrers = fields.List(fields.Nested(UserSchema()))
    requester = fields.Nested(RequesterSchema())
    requester_light = fields.Nested(RequesterSchema())
    accommodation = fields.Nested(AccommodationSchema())
    common_areas = fields.Nested(CommonAreaSchema())
    work_types = fields.List(fields.Nested(WorkTypeSchema()))
    requester_id = auto_field(required=False)
    required_action = auto_field(required=True)
    code_name = fields.String(dump_only=True)
    accommodations_length = fields.Integer(dump_only=True)
    sections_permissions = fields.Nested(SectionsPermissionsSchema, dump_only=True)
    mission_name = fields.String(dump_only=True)

    class Meta:
        model = Project
        include_fk = True
        unknown = EXCLUDE


class ProjectCreationSchema(SQLAlchemyAutoSchema):
    mission = fields.Nested(MissionSchema())
    referrers = fields.List(fields.Nested(UserSchema()))
    requester = fields.Nested(RequesterSchema())
    requester_id = auto_field(required=False)
    required_action = auto_field(required=True)
    work_types = fields.List(fields.Nested(WorkTypeSchema()))

    class Meta:
        model = Project
        include_fk = True
        unknown = EXCLUDE
        additional = ["code_name"]


class ProjectUpdateSchema(SQLAlchemyAutoSchema):
    referrers = fields.List(fields.Nested(UserSchema()))
    requester_id = auto_field(required=False)
    required_action = auto_field(required=True)
    requester = fields.Nested(RequesterSchema())
    work_types = fields.List(fields.Nested(WorkTypeSchema()))

    class Meta:
        model = Project
        include_fk = True
        unknown = EXCLUDE


class ProjectPaginatedSchema(PaginatedSchema):
    items = fields.Nested(ProjectSchema, many=True, dump_only=True)


class ProjectDeleteMultipleSchema(Schema):
    projects_id = fields.List(Integer())


class ProjectAnonymizeMultipleSchema(Schema):
    projects_id = fields.List(Integer())


class ProjectDocumentSchema(DocumentSchema):
    entity_id = fields.Integer(required=False)
