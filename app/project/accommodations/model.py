from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import PhoneNumber, HasPhones


class Accommodation(HasPhones, BaseMixin, db.Model):
    """ Accommodation  """

    __tablename__ = "accommodation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    accommodation_type = Column(String(255), nullable=True)
    condominium = Column(Boolean, nullable=True)
    purchase_year = Column(Integer(), nullable=True)
    construction_year = Column(Integer(), nullable=True)
    levels_nb = Column(Integer, nullable=True)
    rooms_nb = Column(Integer, nullable=True)
    living_area = Column(Float, nullable=True)
    additional_area = Column(Float, nullable=True)
    vacant = Column(Boolean, nullable=True, default=False)
    year_vacant_nb = Column(Integer, nullable=True)
    commentary = Column(String(800), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship(
        "Project", backref=backref("accommodations", cascade="all, delete")
    )
    name = Column(String(255), nullable=True)
    address_complement = Column(String(800), nullable=True)
    typology = Column(String(255), nullable=True)
    degradation_coefficient = Column(Float, nullable=True)
    unsanitary_coefficient = Column(Float, nullable=True)
    current_rent = Column(Float, nullable=True)
    rent_after_renovation = Column(Float, nullable=True)
    type_rent_after_renovation = Column(String(255), nullable=True)
    out_of_project = Column(Boolean(create_constraint=False), nullable=True)
    minors_tenants_number = Column(Integer(), nullable=True)
    adults_tenants_number = Column(Integer(), nullable=True)
    tenant_title = Column(String(10), nullable=True)
    tenant_last_name = Column(String(255), nullable=True)
    tenant_first_name = Column(String(255), nullable=True)
    tenant_email = Column(String(255), nullable=True)
    tenant_commentary = Column(String(800), nullable=True)
    access = Column(String(255), nullable=True)
    case_type = Column(String(255), nullable=True)
    secondary_case_type = Column(String(255), nullable=True)
    disability_card = Column(Boolean(create_constraint=False), nullable=True)
    rate_adaptation = Column(Integer(), nullable=True)
    has_AAH = Column(Boolean(create_constraint=False), nullable=True)
    has_APA = Column(Boolean(create_constraint=False), nullable=True)
    GIR_coefficient = Column(Integer(), nullable=True)

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()

    @hybrid_property
    def initial_state_id(self):
        from app.perrenoud.scenarios.model import Scenario

        initial_state = (
            Scenario.query.filter(Scenario.accommodation_id == self.id)
            .filter(Scenario.is_initial_state == True)
            .first()
        )
        return initial_state.id if initial_state else None

    @hybrid_property
    def initial_state(self):
        from app.perrenoud.scenarios.model import Scenario

        initial_state = (
            Scenario.query.filter(Scenario.accommodation_id == self.id)
            .filter(Scenario.is_initial_state == True)
            .first()
        )
        return initial_state

    @hybrid_property
    def scenarios_list(self):
        from app.perrenoud.scenarios.model import Scenario

        scenarios_list = (
            Scenario.query.filter(Scenario.accommodation_id == self.id)
            .filter(Scenario.is_initial_state == False)
            .all()
        )
        return scenarios_list

    @hybrid_property
    def scenarios_number(self):
        from app.perrenoud.scenarios.model import Scenario

        return len(
            Scenario.query.filter(Scenario.accommodation_id == self.id)
            .filter(Scenario.is_initial_state == False)
            .all()
        )
