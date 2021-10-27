from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from app.common.address.model import Address


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Address

