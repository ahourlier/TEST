from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    case,
    func,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from sqlalchemy.orm import relationship, backref, aliased
from enum import Enum
from sqlalchemy.sql.functions import concat
from app import db
from app.common.base_model import BaseMixin
from app.mission.missions import Mission
from app.project.requesters.model import RequesterTypes

FIELDS_MAPPING = {
    "address_number": '',
    "notes": '',
    "work_type": '',
    "address_street": '',
    "description": '',
    "address_complement": '',
    "active": '',
    "created_at": '',
    "closed": '',
    "monitoring_commentary": '',
    "address_code": '',
    "anonymized": '',
    "closure_motive": '',
    "no_advance_request": '',
    "address_location": '',
    "id": '',
    "urgent_visit": '',
    "drive_init": '',
    "address_latitude": '',
    "status": '',
    "address_longitude": '',
    "address": '',
    "type": '',
    "secondary_case_type": ''
}


class ProjectTypes(Enum):
    SERENITY = "Habiter Mieux Sérénité"
    ADAPTATION = "Adaptation"
    HEAVY_WORK = "Travaux Lourds"
    SECURITY = "Sécurité et Salubrité de l'Habitat"
    MIXTE = "Mixte"
    USE_TRANSFORMATION = "Transformation d'usage"
    PENSION_FOUND = "Caisse de retraite"
    ACTION_ENERGY = "Action Logement/Energie"
    ACTION_ADAPTATION = "Action Logement/Adaptation"
    NONE = "Aucun"
    OTHER = "Autre"


class ProjectStatus(Enum):
    TO_CONTACT = "À Contacter"
    CONTACT = "Contact"
    MEET_ADVICES_TO_PLAN = "Visite conseil à programmer"
    MEET_ADVICES_PLANNED = "Visite conseil programmée"
    MEET_TO_PROCESS = "Visite à traiter"
    BUILD_ON_GOING = "En cours de montage"
    DEPOSITTED = "Déposé"
    CERTIFIED = "Agréé"
    MEET_CONTROL_TO_PLAN = "Visite contrôle à programmer"
    MEET_CONTROL_PLANNED = "Visite contrôle programmée"
    PAYMENT_REQUEST_TO_DO = "Demande paiement à faire"
    ASKING_FOR_PAY = "En demande de paiement"
    CLEARED = "Soldé"
    DISMISSED = "Sans suite"
    NON_ELIGIBLE = "Non éligible"
    OTHER = "Autre"


class ProjectDateStatus(Enum):
    date_meet_advices_to_plan = "Visite conseil à programmer"
    date_meet_control_to_plan = "Visite contrôle à programmer"
    date_to_contact = "À Contacter"
    date_contact = "Contact"
    date_meet_to_process = "Visite à traiter"
    date_build_on_going = "En cours de montage"
    date_depositted = "Déposé"
    date_certified = "Agréé"
    date_meet_advices_planned = "Visite conseil programmée"
    date_meet_control_planned = "Visite contrôle programmée"
    date_payment_request_to_do = "Demande paiement à faire"
    date_asking_for_pay = "En demande de paiement"
    date_cleared = "Soldé"
    date_dismissed = "Sans suite"
    date_non_eligible = "Non éligible"


class Project(BaseMixin, db.Model):
    """ Project  """

    __tablename__ = "project"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    status = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    address_number = Column(String(255), nullable=True)
    address_street = Column(String(255), nullable=True)
    address_complement = Column(String(255), nullable=True)
    address_code = Column(String(255), nullable=True)
    address_location = Column(String(255), nullable=True)
    address_latitude = Column(Float(), nullable=True)
    address_longitude = Column(Float(), nullable=True)
    type = Column(String(255), nullable=True)
    secondary_case_type = Column(String(255), nullable=True)
    work_type = Column(String(255), nullable=True)
    description = Column(String(2083), nullable=True)
    closed = Column(Boolean, nullable=True)
    closure_motive = Column(String(255), nullable=True)
    urgent_visit = Column(Boolean, nullable=True)
    date_advice_meet = db.Column(db.Date, nullable=True)
    date_control_meet = db.Column(db.Date, nullable=True)
    notes = Column(String(2083), nullable=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="projects")
    date_meet_advices_to_plan = db.Column(db.Date, nullable=True)
    date_meet_control_to_plan = db.Column(db.Date, nullable=True)
    date_to_contact = db.Column(db.Date, nullable=True)
    date_contact = db.Column(db.Date, nullable=True)
    date_meet_to_process = db.Column(db.Date, nullable=True)
    date_build_on_going = db.Column(db.Date, nullable=True)
    date_depositted = db.Column(db.Date, nullable=True)
    date_certified = db.Column(db.Date, nullable=True)
    date_meet_advices_planned = db.Column(db.Date, nullable=True)
    date_meet_control_planned = db.Column(db.Date, nullable=True)
    date_payment_request_to_do = db.Column(db.Date, nullable=True)
    date_asking_for_pay = db.Column(db.Date, nullable=True)
    date_cleared = db.Column(db.Date, nullable=True)
    date_dismissed = db.Column(db.Date, nullable=True)
    date_non_eligible = db.Column(db.Date, nullable=True)
    requester_id = Column(
        Integer, ForeignKey("requester.id"), unique=True, nullable=False
    )
    requester = relationship(
        "Requester", backref=backref("project", uselist=False), cascade="all, delete"
    )
    active = Column(Boolean(create_constraint=False), default=True, nullable=False)
    anonymized = Column(Boolean(create_constraint=False), default=False, nullable=True)
    sd_root_folder_id = db.Column(String(255), nullable=True)
    sd_quotes_folder_id = db.Column(String(255), nullable=True)
    sd_accommodation_folder_id = db.Column(String(255), nullable=True)
    sd_accommodation_report_folder_id = db.Column(String(255), nullable=True)
    sd_accommodation_pictures_folder_id = db.Column(String(255), nullable=True)
    sd_funders_folder_id = db.Column(String(255), nullable=True)
    sd_requester_folder_id = db.Column(String(255), nullable=True)
    monitoring_commentary = Column(String(2083), nullable=True)
    no_advance_request = Column(Boolean, nullable=True)
    drive_init = db.Column(String(255), default="TODO")

    @hybrid_property
    def referrers(self):
        return [s.user for s in self.project_leads]

    @hybrid_property
    def code_name(self):
        return f"{self.mission.code_name}-{self.id}"

    @code_name.expression
    def code_name(cls):
        mission_alias = aliased(Mission)
        return (
            select([concat(mission_alias.code_name, "-", cls.id)])
                .where(mission_alias.id == cls.mission_id)
                .label("code_name")
        )

    @hybrid_property
    def accommodation(self):
        if (
                self.requester.type != RequesterTypes.PB.value
                and len(self.accommodations) > 0
        ):
            return self.accommodations[0]
        else:
            return None

    @hybrid_property
    def owner_accommodations(self):
        if self.requester.type == RequesterTypes.PB.value:
            return self.accommodations
        else:
            return None

    @hybrid_property
    def accommodations_length(self):
        return len(self.accommodations)

    @hybrid_property
    def sections_permissions(self):
        return {
            "ca_requester": self.mission.ca_requester,
            "ca_accommodation": self.mission.ca_accommodation,
            "ca_common_area": self.mission.ca_common_area,
            "ca_accommodation_summary": self.mission.ca_accommodation_summary,
            "ca_quotes": self.mission.ca_quotes,
            "ca_simulations": self.mission.ca_simulations,
            "ca_deposit": self.mission.ca_deposit,
            "ca_certification": self.mission.ca_certification,
            "ca_payment_request": self.mission.ca_payment_request,
            "ca_funders": self.mission.ca_funders,
            "ca_documents": self.mission.ca_documents,
            "ca_follow_up": self.mission.ca_follow_up,
        }

    @hybrid_property
    def mission_name(self):
        return self.mission.name

    @hybrid_property
    def requester_light(self):
        return {
            "last_name": self.requester.last_name,
            "first_name": self.requester.first_name,
            "type": self.requester.type,
            "date_contact": self.requester.date_contact,
            "resources_category": self.requester.resources_category,
        }
