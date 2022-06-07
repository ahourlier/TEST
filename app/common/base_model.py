from datetime import datetime

from mypy_extensions import TypedDict
from sqlalchemy.event import listens_for

from app import db


class BaseMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, changes: TypedDict):
        for key, val in changes.items():
            if key == "id":
                continue
            setattr(self, key, val)

        return self


@listens_for(db.Model, "before_update", propagate=True)
def before_update_function(mapper, connection, target):
    target.updated_at = datetime.utcnow()


class SoftDeletableMixin:
    """Add this mixin to make an entity soft deletable"""

    is_deleted = db.Column(db.Boolean, default=False)

    def soft_delete(self):
        self.is_deleted = True
