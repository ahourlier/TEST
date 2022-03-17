from typing import List

import app.project.accommodations.service as accommodation_service
from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.project.disorders import Disorder, DisorderType

from app.project.disorders.error_handlers import (
    DisorderNotFoundException,
    DisorderTypeNotFoundException,
)
from app.project.disorders.exceptions import InvalidDisorderJoinException
from app.project.disorders.interface import DisorderInterface, DisorderTypeInterface
import app.project.common_areas.service as common_area_service


class DisorderService:
    @staticmethod
    def create(new_attrs: DisorderInterface) -> Disorder:
        """Create a new disorder linked to an accommodation or a common area"""
        if "accommodation_id" in new_attrs and "common_area_id" not in new_attrs:
            accommodation_service.AccommodationService.get_by_id(
                new_attrs.get("accommodation_id")
            )
        elif "common_area_id" in new_attrs and "accommodation_id" not in new_attrs:
            common_area_service.CommonAreaService.get_by_id(
                new_attrs.get("common_area_id")
            )
        else:
            raise InvalidDisorderJoinException()

        disorder_obj = dict(new_attrs)
        del disorder_obj["analysis_types"]
        del disorder_obj["recommendation_types"]

        disorder = Disorder(**disorder_obj)

        db.session.add(disorder)
        db.session.commit()

        DisorderTypeService.create_list(
            new_attrs.get("analysis_types"),
            new_attrs.get("recommendation_types"),
            disorder.id,
        )

        return disorder

    @staticmethod
    def create_list(
        new_disorders: List[DisorderInterface],
        accommodation_id=None,
        common_area_id=None,
    ) -> List[Disorder]:
        """Create disorders from a list"""
        if accommodation_id is not None and common_area_id is None:
            parent_id_key = "accommodation_id"
            parent_id = accommodation_id
        elif common_area_id is not None and accommodation_id is None:
            parent_id_key = "common_area_id"
            parent_id = common_area_id
        else:
            raise InvalidDisorderJoinException()

        disorders = []
        for disorder in new_disorders:
            disorder[parent_id_key] = parent_id
            disorders.append(DisorderService.create(disorder))

        return disorders

    @staticmethod
    def get_by_id(disorder_id: str) -> Disorder:
        db_disorder = Disorder.query.get(disorder_id)
        if db_disorder is None:
            raise DisorderNotFoundException
        return db_disorder

    @staticmethod
    def update(
        disorder: Disorder, changes: DisorderInterface, force_update: bool = False
    ) -> Disorder:
        if force_update or DisorderService.has_changed(disorder, changes):
            # If one tries to update entity id, an error must be raised
            if changes.get("id") and changes.get("id") != disorder.id:
                raise InconsistentUpdateIdException()

            # We don't want tu update disorder's parent
            if "accommodation_id" in changes:
                del changes["accommodation_id"]
            if "common_area_id" in changes:
                del changes["common_area_id"]

            disorder.update(changes)
            db.session.commit()
        return disorder

    @staticmethod
    def update_list(
        list_changes, accommodation_id: int = None, common_area_id: int = None,
    ):
        # We deal with cases where parent is an accommodation OR common_area
        if accommodation_id is not None and common_area_id is None:
            old_disorders = Disorder.query.filter_by(
                accommodation_id=accommodation_id,
            ).all()
            parent_id_key = "accommodation_id"
            parent_id = accommodation_id
        elif common_area_id is not None and accommodation_id is None:
            parent_id_key = "common_area_id"
            parent_id = common_area_id
            old_disorders = Disorder.query.filter_by(
                common_area_id=common_area_id,
            ).all()
        else:
            raise InvalidDisorderJoinException()

        for disorder_changes in list_changes:
            # If disorder exists, it must be updated
            if "id" in disorder_changes:
                disorder = DisorderService.get_by_id(disorder_changes["id"])
                analysis_types = []
                recommendation_types = []

                del disorder_changes["disorder_types"]
                if "analysis_types" in disorder_changes:
                    analysis_types = disorder_changes["analysis_types"]
                    del disorder_changes["analysis_types"]
                if "recommendation_types" in disorder_changes:
                    recommendation_types = disorder_changes["recommendation_types"]
                    del disorder_changes["recommendation_types"]
                DisorderTypeService.update_list(
                    analysis_types, recommendation_types, disorder.id,
                )

                DisorderService.update(disorder, disorder_changes)
            # Else, it must be created
            else:
                disorder_changes[parent_id_key] = parent_id
                DisorderService.create(disorder_changes)

        is_removed = True
        for old_disorder in old_disorders:
            if not list_changes:
                DisorderService.delete_by_id(old_disorder.id)
            for new_disorder in list_changes:
                if "id" in new_disorder and new_disorder["id"] == old_disorder.id:
                    is_removed = False
                    break
                if is_removed:
                    DisorderService.delete_by_id(old_disorder.id)

    @staticmethod
    def has_changed(disorder: Disorder, changes: DisorderInterface) -> bool:
        for key, value in changes.items():
            if getattr(disorder, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(disorder_id: int) -> int or None:
        disorder = Disorder.query.filter(Disorder.id == disorder_id).first()
        if not disorder:
            raise DisorderNotFoundException

        old_disorder_types = DisorderType.query.filter(disorder_id == disorder.id).all()

        for old_disorder_type in old_disorder_types:
            DisorderTypeService.delete_by_id(old_disorder_type.id)

        db.session.delete(disorder)
        db.session.commit()
        return disorder_id


class DisorderTypeService:
    @staticmethod
    def create(new_attrs: DisorderTypeInterface) -> DisorderType:
        DisorderService.get_by_id(new_attrs.get("disorder_id"))

        disorder_type = DisorderType(**new_attrs)
        db.session.add(disorder_type)
        db.session.commit()
        return disorder_type

    @staticmethod
    def create_list(
        analysis_types: List[DisorderTypeInterface],
        recommendation_types: List[DisorderTypeInterface],
        disorder_id: int,
    ) -> List[DisorderType]:
        analysis = analysis_types if analysis_types else []
        recommendations = recommendation_types if recommendation_types else []

        disorder_type = analysis + recommendations

        # Create corresponding disorder types
        disorder_types = []
        for analysis in disorder_type:
            analysis["disorder_id"] = disorder_id
            disorder_types.append(DisorderTypeService.create(analysis))

        return disorder_types

    @staticmethod
    def update_list(analysis_types, recommendation_types, disorder_id):

        # Delete
        old_disorder_types = DisorderType.query.filter(
            DisorderType.disorder_id == disorder_id
        ).all()
        for old_disorder_type in old_disorder_types:
            DisorderTypeService.delete_by_id(old_disorder_type.id)

        # Re-create
        for a in analysis_types:
            a["disorder_id"] = disorder_id
            DisorderTypeService.create(a)

        for r in recommendation_types:
            r["disorder_id"] = disorder_id
            DisorderTypeService.create(r)

    @staticmethod
    def delete_by_id(disorder_type_id: int) -> int or None:
        disorder_type = DisorderType.query.filter(
            DisorderType.id == disorder_type_id
        ).first()
        if not disorder_type:
            raise DisorderTypeNotFoundException
        db.session.delete(disorder_type)
        db.session.commit()
        return disorder_type_id
