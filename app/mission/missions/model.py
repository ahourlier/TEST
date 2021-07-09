from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    SmallInteger,
    select,
    case,
    func,
    Boolean,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import concat

from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin

# for relationships
from app.admin.antennas import Antenna


class MissionStatus:
    NOT_STARTED = "Non débutée"
    ON_GOING = "En cours"
    POST_OPERATION = "Post opération"
    ARCHIVED = "Archivée"


class Mission(SoftDeletableMixin, BaseMixin, db.Model):
    """ Mission  """

    __tablename__ = "mission"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    status = Column(String(255), nullable=False, default=MissionStatus.NOT_STARTED)
    name = Column(String(255), nullable=True)
    agency_id = Column(Integer, ForeignKey("agency.id"), nullable=True)
    agency = relationship("Agency", backref="missions")
    antenna_id = Column(Integer, ForeignKey("antenna.id"), nullable=True)
    antenna = relationship("Antenna", backref="missions")
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=True)
    client = db.relationship("Client", backref="missions")
    comment = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    sd_root_folder_id = db.Column(String(255), nullable=True)
    sd_document_templates_folder_id = db.Column(String(255), nullable=True)
    sd_information_documents_folder_id = db.Column(String(255), nullable=True)
    sd_projects_folder_id = db.Column(String(255), nullable=True)
    google_group_id = db.Column(String(255), nullable=True)
    ca_requester = db.Column(Boolean, nullable=True, default=False)
    ca_accommodation = db.Column(Boolean, nullable=True, default=False)
    ca_common_area = db.Column(Boolean, nullable=True, default=False)
    ca_accommodation_summary = db.Column(Boolean, nullable=True, default=False)
    ca_quotes = db.Column(Boolean, nullable=True, default=False)
    ca_simulations = db.Column(Boolean, nullable=True, default=False)
    ca_deposit = db.Column(Boolean, nullable=True, default=False)
    ca_certification = db.Column(Boolean, nullable=True, default=False)
    ca_payment_request = db.Column(Boolean, nullable=True, default=False)
    ca_funders = db.Column(Boolean, nullable=True, default=False)
    ca_documents = db.Column(Boolean, nullable=True, default=False)
    ca_follow_up = db.Column(Boolean, nullable=True, default=False)
    drive_init = db.Column(String(255), default="TODO")
    creator = db.Column(String(255), nullable=True)

    @hybrid_property
    def code_name(self):
        code_name = f"{self.agency.code_name}" if self.agency else ""
        code_name = (
            f"{code_name}-{self.antenna.code_name}" if self.antenna else code_name
        )
        code_name = f"{code_name}-{self.id}"
        return code_name

    @code_name.expression
    def code_name(cls):
        return case(
            [
                (
                    cls.antenna_id != None,
                    concat(cls.agency_id, "-", cls.antenna_id, "-", cls.id),
                )
            ],
            else_=concat(cls.agency_id, "-", cls.id),
        )

    @code_name.expression
    def mission_managers(cls):
        return case(
            [
                (
                    cls.antenna_id != None,
                    concat(cls.agency_id, "-", cls.antenna_id, "-", cls.id),
                )
            ],
            else_=concat(cls.agency_id, "-", cls.id),
        )
