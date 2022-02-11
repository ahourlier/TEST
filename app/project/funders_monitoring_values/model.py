from datetime import date, datetime

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin
from app.common.constants import DATE_FORMAT
from app.mission.monitors.model import MonitorField  # To keep for import purpose


class FunderMonitoringValue(BaseMixin, db.Model):
    """FundersMonitoringValues"""

    __tablename__ = "funders_monitoring_values"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship("Project", backref="funders_monitoring_values")
    funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    funder = relationship("Funder", backref="projects_monitoring_values")
    monitor_field_id = Column(Integer, ForeignKey("monitor_field.id"), nullable=True)
    monitor_field = relationship("MonitorField", backref="values")
    date_value = db.Column(db.Date, nullable=True)
    boolean_value = Column(Boolean, nullable=True)

    @hybrid_property
    def value(self):
        # We use "value" property has a tool for dispatching good value :
        # Base fetched value if the monitor field is automatic
        # / date_value or boolean_value, depending on type
        if self.monitor_field.automatic is True:
            automatic_date = FunderMonitoringValue.get_automatic_value(
                self.project, self.funder, self.monitor_field.name
            )
            return (
                automatic_date.strftime(DATE_FORMAT)
                if automatic_date is not None
                else automatic_date
            )
        else:
            if self.monitor_field.type == "boolean":
                return self.boolean_value
            else:
                return (
                    self.date_value.strftime(DATE_FORMAT)
                    if self.date_value is not None
                    else None
                )

    @value.setter
    def value(self, value):
        # We use "value" property has a tool for dispatching value into the right property :
        # date_value or boolean_value, depending on type
        # Automatic field are just ignored
        if self.monitor_field.automatic is False:
            if self.monitor_field.type == "boolean":
                self.boolean_value = value
            else:
                if value is not None:
                    self.date_value = datetime.strptime(value, DATE_FORMAT)
                else:
                    self.date_value = None

    @staticmethod
    def get_automatic_value(project, funder, monitor_field_name):
        # "Dépôt", "Agrément" and ""Envoi demande de paiement" are special values :
        # They cannot be filled by user. Instead, they are fetched from simulations tables.
        if monitor_field_name == "Dépôt":
            # Return the last added deposit_date for this project and this funder
            deposit_funders = []
            for simulation in project.simulations:
                for deposit_funder in simulation.deposit_funders:
                    if deposit_funder.funder.id == funder.id:
                        deposit_funders.append(deposit_funder)

            if len(deposit_funders) > 0:
                deposit_funders.sort(key=lambda x: x.id, reverse=True)
                return deposit_funders[0].deposit_date
            else:
                return None
        elif monitor_field_name == "Agrément":
            # Return the last added payment_request_date for this project and this funder
            certification_funders = []
            for simulation in project.simulations:
                for certification_funder in simulation.certification_funders:
                    if certification_funder.funder.id == funder.id:
                        certification_funders.append(certification_funder)

            if len(certification_funders) > 0:
                certification_funders.sort(key=lambda x: x.id, reverse=True)
                return certification_funders[0].certification_date
            else:
                return None
        elif monitor_field_name == "Envoi demande de paiement":
            # Return the last added payment_request_date for this project and this funder
            payment_request_funders = []
            for simulation in project.simulations:
                for payment_request_funder in simulation.payment_request_funders:
                    if payment_request_funder.funder.id == funder.id:
                        payment_request_funders.append(payment_request_funder)

            if len(payment_request_funders) > 0:
                payment_request_funders.sort(key=lambda x: x.id, reverse=True)
                return payment_request_funders[0].payment_request_date
            else:
                return None
        else:
            return None
