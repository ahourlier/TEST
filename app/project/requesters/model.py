from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Float, select
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class RequesterTypes(Enum):
    PO = "PO"
    PB = "PB"
    TENANT = "LOCATAIRE"
    SDC = "SDC (Syndicat des Copropriétaires)"


class Requester(HasPhones, BaseMixin, db.Model):
    """ Requester  """

    __tablename__ = "requester"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    title = Column(String(10), nullable=True)
    birthday_date = db.Column(db.Date, nullable=True)
    type = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    address_number = Column(String(255), nullable=True)
    address_street = Column(String(255), nullable=True)
    address_complement = Column(String(255), nullable=True)
    address_code = Column(String(255), nullable=True)
    address_location = Column(String(255), nullable=True)
    address_latitude = Column(Float(), nullable=True)
    address_longitude = Column(Float(), nullable=True)
    cadastral_reference = Column(String(255), nullable=True)
    date_contact = db.Column(db.Date, nullable=True)
    contact_source = Column(String(255), nullable=True)
    minors_occupants_number = Column(Integer(), nullable=True)
    adults_occupants_number = Column(Integer(), nullable=True)
    profession = Column(String(255), nullable=True)
    resources_category = Column(String(255), nullable=True)
    non_eligible = Column(Boolean(create_constraint=False), nullable=True)
    ineligibility = Column(String(255), nullable=True)
    PTZ_year = db.Column(Integer(), nullable=True)
    is_private = Column(Boolean(create_constraint=False), nullable=True)
    company_name = Column(String(255), nullable=True)
    disability_card = Column(Boolean(create_constraint=False), nullable=True)
    rate_adaptation = Column(Integer(), nullable=True)
    has_AAH = Column(Boolean(create_constraint=False), nullable=True)
    has_APA = Column(Boolean(create_constraint=False), nullable=True)
    GIR_coefficient = Column(Integer(), nullable=True)

    @hybrid_property
    def phone_number_1(self):
        return self.phones[0] if self.phones else None

    @phone_number_1.expression
    def phone_number_1(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()

    @hybrid_property
    def phone_number_2(self):
        return self.phones[1] if self.phones and len(self.phones) > 1 else None

    @phone_number_2.expression
    def phone_number_2(cls):
        return (
            select([PhoneNumber])
            .where(PhoneNumber.resource_id == cls.id)
            .order_by(PhoneNumber.id.desc())
            .first()
        )

    @hybrid_property
    def project_type(self):
        return self.project.type
