from flask import jsonify

from app.referential.enums import AppEnum

ENUM_NAME = "Job"


class JobService:
    @staticmethod
    def get_all():
        return jsonify(
            [
                {
                    "value": enum.name,
                    "display_order": enum.display_order,
                    "disabled": enum.disabled,
                    "private": enum.private,
                }
                for enum in AppEnum.query.filter(AppEnum.kind == ENUM_NAME).all()
            ]
        )
