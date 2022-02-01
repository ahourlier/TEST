from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship, validates, backref

from app import db
from app.common.base_model import BaseMixin

from app.common.config_error_messages import (
    KEY_FUNDING_SCENARIO_INVALID_RATE,
    KEY_FUNDING_SCENARIO_INVALID_CRITERIA,
)


FUNDING_SCENARIOS_CRITERIA_CONFIGURATION = {
    "requester.resources_category": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectRequesterResourceCategory",
        "field_model": "Requester",
        "field_ref": "resources_category",
    },
    "address_location": {
        "type": "string",
        "operators": ["="],
        "field_model": "Project",
        "field_ref": "address_location",
    },
    "accommodations.vacant": {
        "type": "bool",
        "operators": ["="],
        "field_model": "Accommodation",
        "field_ref": "vacant",
    },
    "accommodations.purchase_year": {
        "type": "date-year",
        "operators": ["<", "<=", "=", ">=", ">"],
        "field_model": "Accommodation",
        "field_ref": "purchase_year",
    },
    "work_types.type_name": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectWorksType",
        "field_model": "Project",
        "field_ref": "work_types",
    },
    "requester.profession": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectRequesterProfessionType",
        "field_model": "Requester",
        "field_ref": "profession",
    },
    "type": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectCaseType",
        "field_model": "Project",
        "field_ref": "type",
    },
    "secondary_case_type": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectCaseType",
        "field_model": "Project",
        "field_ref": "secondary_case_type",
    },
    "accommodations.type_rent_after_renovation": {
        "type": "enum",
        "operators": ["="],
        "enumKind": "ProjectAccommodationRentTypeAfterRenovation",
        "field_model": "Accommodation",
        "field_ref": "type_rent_after_renovation",
    },
}


class FundingScenario(BaseMixin, db.Model):
    """Represents a scenario for a funder"""

    __tablename__ = "funding_scenario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    criteria = Column(JSON, nullable=False)
    rate = Column(Integer, nullable=False, default=100)
    upper_limit = Column(Integer, nullable=True)
    advance = Column(Integer, nullable=True)
    upper_surface_limit = Column(Integer, nullable=True)
    upper_price_surface_limit = Column(Integer, nullable=True)
    funder_id = Column(Integer, ForeignKey("funder.id"), nullable=False)
    funder = relationship(
        "Funder", backref=backref("funding_scenarios", cascade="all,delete")
    )

    @validates("rate")
    def validate_rate(self, key, value):
        if value > 100 or value < 0:
            raise AssertionError(KEY_FUNDING_SCENARIO_INVALID_RATE)
        return value

    @validates("criteria")
    def validate_criteria(self, key, value):
        if not isinstance(value, list):
            raise AssertionError(KEY_FUNDING_SCENARIO_INVALID_CRITERIA)
        for criterion in value:
            keys = criterion.keys()
            if "field" not in keys or "operator" not in keys or "value" not in keys:
                raise AssertionError(KEY_FUNDING_SCENARIO_INVALID_CRITERIA)
            if criterion["field"] not in FUNDING_SCENARIOS_CRITERIA_CONFIGURATION:
                raise AssertionError(KEY_FUNDING_SCENARIO_INVALID_CRITERIA)
            if (
                criterion["operator"]
                not in FUNDING_SCENARIOS_CRITERIA_CONFIGURATION[criterion["field"]][
                    "operators"
                ]
            ):
                raise AssertionError(KEY_FUNDING_SCENARIO_INVALID_CRITERIA)
        return value
