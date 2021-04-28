from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.project.common_areas import CommonArea
from app.project.common_areas.error_handlers import (
    CommonAreaNotFoundException,
    ExistingCommonAreaException,
)
from app.project.common_areas.interface import CommonAreaInterface
import app.project.projects.service as projects_service
import app.project.disorders.service as disorders_service


class CommonAreaService:
    @staticmethod
    def create(new_attrs: CommonAreaInterface, project_id: int) -> CommonArea:
        """ Create a new common_area """
        common_area_fields = CommonAreaInterface(**new_attrs)
        disorders = []
        if "disorders" in common_area_fields:
            disorders = common_area_fields["disorders"]
            del common_area_fields["disorders"]

        # Project link
        project = projects_service.ProjectService.get_by_id(project_id)
        if project.common_areas is not None:
            raise ExistingCommonAreaException()
        common_area_fields["project_id"] = project_id

        common_area = CommonArea(**common_area_fields)
        db.session.add(common_area)
        db.session.commit()

        # Create linked disorders
        disorders_service.DisorderService.create_list(
            disorders, common_area_id=common_area.id
        )

        return common_area

    @staticmethod
    def get_by_id(common_area_id: str) -> CommonArea:
        db_common_area = CommonArea.query.get(common_area_id)
        if db_common_area is None:
            raise CommonAreaNotFoundException()
        return db_common_area

    @staticmethod
    def update(
        common_area: CommonArea,
        changes: CommonAreaInterface,
        force_update: bool = False,
    ) -> CommonArea:
        if force_update or CommonAreaService.has_changed(common_area, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != common_area.id:
                raise InconsistentUpdateIdException()

            # Update disorders
            if "disorders" in changes:
                disorders_service.DisorderService.update_list(
                    changes["disorders"], common_area_id=common_area.id
                )
                del changes["disorders"]

            common_area.update(changes)
            db.session.commit()
        return common_area

    @staticmethod
    def has_changed(common_area: CommonArea, changes: CommonAreaInterface) -> bool:
        for key, value in changes.items():
            if getattr(common_area, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(common_area_id: int) -> int or None:
        common_area = CommonArea.query.filter(CommonArea.id == common_area_id).first()
        if not common_area:
            raise CommonAreaNotFoundException
        db.session.delete(common_area)
        db.session.commit()
        return common_area_id
