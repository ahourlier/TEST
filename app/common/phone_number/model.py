from sqlalchemy import Column, Integer, String, event, desc
from sqlalchemy.orm import relationship, foreign, remote, backref
from sqlalchemy import and_

from app import db
from app.common.base_model import BaseMixin


class PhoneNumber(BaseMixin, db.Model):
    """Represents a phone number"""

    __tablename__ = "phone_number"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String(3), nullable=True)
    national = Column(String(128), nullable=True)
    international = Column(String(128), nullable=True)
    kind = Column(String(128), nullable=True)
    resource_type = Column(String(128), nullable=True)
    resource_id = Column(Integer, nullable=True)

    @property
    def resource(self):
        """Provides access to the "parent" resource by using the proper relationship"""
        return getattr(self, f"resource_{self.resource_type}")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(country_code={self.country_code}, "
            f"national={self.national}, "
            f"international={self.international}, "
            f"kind={self.kind})"
        )


class HasPhones:
    """Placeholder mixin that will create a relationship to
    the phone_number_association table for each resource

    """


@event.listens_for(HasPhones, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    resource_type = name.lower()
    class_.phones = relationship(
        PhoneNumber,
        primaryjoin=and_(
            class_.id == foreign(remote(PhoneNumber.resource_id)),
            PhoneNumber.resource_type == resource_type,
        ),
        backref=backref(
            f"resource_{resource_type}",
            primaryjoin=remote(class_.id) == foreign(PhoneNumber.resource_id),
        ),
        cascade="all, delete",
        order_by=PhoneNumber.id,
    )

    @event.listens_for(class_.phones, "append")
    def append_phone_number(target, value, initiator):
        value.resource_type = resource_type
