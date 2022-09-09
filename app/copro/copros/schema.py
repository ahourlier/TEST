import base64
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.building.settings import NB_LOOP_ACCESS_CODE
from app.copro.architect.schema import (
    ArchitectCreateSchema,
    ArchitectSchema,
    ArchitectUpdateSchema,
)
from app.copro.caretaker.schema import (
    CareTakerCreateSchema,
    CareTakerSchema,
    CareTakerUpdateSchema,
)
from app.copro.employee.schema import (
    EmployeeCreateSchema,
    EmployeeSchema,
    EmployeeUpdateSchema,
)
from app.copro.fire_safety_personnel.schema import (
    FireSafetyPersonnelCreateSchema,
    FireSafetyPersonnelSchema,
    FireSafetyPersonnelUpdateSchema,
)

from .model import Copro, UrbanisCollaborators
from ..cadastre.schema import CadastreSchema
from ..moe.schema import MoeSchema, MoeUpdateSchema, MoeCreateSchema
from ..president.schema import PresidentSchema, PresidentCreateSchema
from ...auth.users.schema import UserSchema
from ...common.phone_number.schema import PhoneNumberSchema
from ...cle_repartition.schema import CleRepartitionSchema, CleRepartitionCreateSchema
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema(), dump_only=True)
    cadastres = fields.List(fields.Nested(CadastreSchema()), dump_only=True)
    access_code = fields.Method("decode_access_code", dump_only=True)

    def decode_access_code(self, obj):
        if not obj.access_code or obj.access_code == "":
            return ""
        access_code = obj.access_code
        for _ in range(0, NB_LOOP_ACCESS_CODE):
            access_code = base64.b64decode(access_code)
        return access_code.decode()

    address_1 = fields.Nested(AddressSchema(), dump_only=True)
    address_2 = fields.Nested(AddressSchema(), dump_only=True)
    syndic_manager_address = fields.Nested(AddressSchema(), dump_only=True)
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), dump_only=True)
    admin_manager_address = fields.Nested(AddressSchema(), dump_only=True)
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), dump_only=True)

    urbanis_collaborators = fields.List(fields.Nested(UserSchema()), dump_only=True)

    moe = fields.Nested(MoeSchema(), dump_only=True)
    architect = fields.Nested(ArchitectSchema(), required=False, allow_none=True)
    caretaker = fields.Nested(CareTakerSchema(), required=False, allow_none=True)
    employee = fields.Nested(EmployeeSchema(), required=False, allow_none=True)
    fire_safety_personnel = fields.Nested(
        FireSafetyPersonnelSchema(), required=False, allow_none=True
    )
    cles_repartition = fields.List(fields.Nested(CleRepartitionSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproUpdateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(
        fields.Nested(CadastreSchema()), allow_none=True, required=False
    )
    address_1 = fields.Nested(AddressSchema(), allow_none=True, required=False)
    address_2 = fields.Nested(AddressSchema(), allow_none=True, required=False)
    syndic_manager_address = fields.Nested(
        AddressSchema(), allow_none=True, required=False
    )
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    admin_manager_address = fields.Nested(
        AddressSchema(), allow_none=True, required=False
    )
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    mission_id = fields.Integer(allow_none=True, required=False)
    president = fields.Nested(PresidentCreateSchema(), allow_none=True, required=False)
    moe = fields.Nested(MoeUpdateSchema(), required=False, allow_none=True)
    architect = fields.Nested(ArchitectUpdateSchema(), required=False, allow_none=True)
    caretaker = fields.Nested(CareTakerUpdateSchema(), required=False, allow_none=True)
    employee = fields.Nested(EmployeeUpdateSchema(), required=False, allow_none=True)
    fire_safety_personnel = fields.Nested(
        FireSafetyPersonnelUpdateSchema(), required=False, allow_none=True
    )
    cles_repartition = fields.List(fields.Nested(CleRepartitionCreateSchema()))
    urbanis_collaborators = fields.List(fields.Nested(UserSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema(), required=False, allow_none=True)
    syndic_manager_address = fields.Nested(
        AddressSchema(), allow_none=True, required=False
    )
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    admin_manager_address = fields.Nested(
        AddressSchema(), allow_none=True, required=False
    )
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    president = fields.Nested(PresidentCreateSchema())
    copro_type = fields.String(required=True, allow_none=False)
    moe = fields.Nested(MoeCreateSchema(), required=False, allow_none=True)
    architect = fields.Nested(ArchitectCreateSchema(), required=False, allow_none=True)
    caretaker = fields.Nested(CareTakerCreateSchema(), required=False, allow_none=True)
    employee = fields.Nested(EmployeeCreateSchema(), required=False, allow_none=True)
    fire_safety_personnel = fields.Nested(
        FireSafetyPersonnelCreateSchema(), required=False, allow_none=True
    )
    cles_repartition = fields.List(fields.Nested(CleRepartitionCreateSchema()))
    urbanis_collaborators = fields.List(fields.Nested(UserSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproForLotsSchema(SQLAlchemyAutoSchema):
    address_1 = fields.Nested(AddressSchema())
    urbanis_collaborators = fields.List(fields.Nested(UserSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproLightSchema(SQLAlchemyAutoSchema):
    address_1 = fields.Nested(AddressSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
