from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from app.admin.antennas import AntennaSchema
from app.common.schemas import PaginatedSchema
from app.person.model import Person
from app.common.phone_number.schema import PhoneNumberSchema


class PersonSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    antenna = fields.Nested(AntennaSchema(), allow_none=True, required=False)

    class Meta:
        model = Person


class PersonPaginatedSchema(PaginatedSchema):
    items = fields.Nested(PersonSchema, many=True, dump_only=True)
