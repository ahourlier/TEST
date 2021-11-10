from flask import jsonify

from app.mission.missions.mission_details.subjob.model import Subjob
from app.referential.enums import AppEnum

ENUM_NAME = "Subjob"


class SubjobService:
    @staticmethod
    def get_all():
        return jsonify([
            {
                "value": enum.name,
                "display_order": enum.display_order,
                "disabled": enum.disabled,
                "private": enum.private
            }
            for enum in AppEnum.query.filter(AppEnum.kind == ENUM_NAME).all()])
