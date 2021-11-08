from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE

from app.mission.missions.mission_details.job.model import Job


class JobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        include_fk = True
        unknown = EXCLUDE
