from typing import List
from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
from app.common.services_utils import ServicesUtils
from app.perrenoud.areas import Area
from app.perrenoud.areas.exceptions import AreaNotFoundException
from app.perrenoud.areas.interface import AreaInterface
import app.perrenoud.rooms.service as rooms_service
import app.perrenoud.room_inputs.service as rooms_input_service


class AreaService:
    @staticmethod
    def get_by_id(area_id: str) -> Area:
        db_area = Area.query.get(area_id)
        if db_area is None:
            raise AreaNotFoundException
        return db_area

    @staticmethod
    def create(
        new_attrs: AreaInterface, room_id=None, room_input_id=None, commit=True
    ) -> Area:
        """ Create a new area"""
        if room_id is not None:
            new_attrs["room_id"] = room_id
            rooms_service.RoomService.get_by_id(new_attrs.get("room_id"))
        if room_input_id is not None:
            new_attrs["room_input_id"] = room_input_id
            rooms_input_service.RoomInputService.get_by_id(
                new_attrs.get("room_input_id")
            )
        area = Area(**new_attrs)
        db.session.add(area)
        if commit:
            db.session.commit()
        return area

    @staticmethod
    def update(area: Area, changes: AreaInterface, force_update: bool = False) -> Area:
        if force_update or AreaService.has_changed(area, changes):
            ServicesUtils.clean_attrs(changes, ["room_id", "room_input_id"])
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != area.id:
                raise InconsistentUpdateIdException()
            area.update(changes)
            db.session.commit()
        return area

    @staticmethod
    def has_changed(area: Area, changes: AreaInterface) -> bool:
        for key, value in changes.items():
            if getattr(area, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(area_id: int) -> int or None:
        area = Area.query.filter(Area.id == area_id).first()
        if not area:
            raise AreaNotFoundException
        db.session.delete(area)
        db.session.commit()
        return area_id

    @staticmethod
    def create_update_list(changes: List, room_input_id=None, room_id=None):
        room_input = None
        room = None
        if room_input_id:
            room_input = rooms_input_service.RoomInputService.get_by_id(room_input_id)
        if room_id:
            room = rooms_service.RoomService.get_by_id(room_id)
        parent = room_input if room_input is not None else room
        original_areas_id = [value.id for value in parent.areas]
        changes_areas_id = [
            areas_fields["id"] for areas_fields in changes if "id" in areas_fields
        ]

        for area_fields in changes:
            # Create
            if "id" not in area_fields:
                if room_input:
                    AreaService.create(area_fields.copy(), room_input_id=room_input.id)
                elif room:
                    AreaService.create(area_fields.copy(), room_id=room.id)
            # Update
            else:
                area = AreaService.get_by_id(area_fields["id"])
                AreaService.update(area, area_fields.copy())

        # Delete obsolete areas
        for original_id in original_areas_id:
            if original_id not in changes_areas_id:
                AreaService.delete_by_id(original_id)

        return parent.areas

    @staticmethod
    def duplicate(
        base_area,
        clone_room_parent_id=None,
        clone_room_input_parent_id=None,
        clone_wall_parent_id=None,
        clone_ceiling_parent_id=None,
    ):
        """ Duplicate an area"""
        if not base_area:
            return
        fields_to_treat_separately = [
            "room_id",
            "room_input_id",
            "wall_id",
            "ceiling_id",
        ]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_area, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["room_id"] = clone_room_parent_id
        base_fields["room_input_id"] = clone_room_input_parent_id
        base_fields["wall_id"] = clone_wall_parent_id
        base_fields["ceiling_id"] = clone_ceiling_parent_id
        clone_area = AreaService.create(base_fields, commit=False)
        db.session.flush()
        return clone_area

    @staticmethod
    def duplicate_all_from_room_or_room_input(
        children_id_maps,
        base_room=None,
        clone_room=None,
        base_room_input=None,
        clone_room_input=None,
    ):
        """Duplicate all areas from base_room and/or base_room_input"""
        if base_room and clone_room:
            for area in base_room.areas:
                AreaService.duplicate(
                    base_area=area, clone_room_parent_id=clone_room.id
                )
        if base_room_input and clone_room_input:
            for area in base_room_input.areas:
                clone_wall_parent_id = None
                clone_ceiling_parent_id = None
                if area.wall_id:
                    clone_wall_parent_id = children_id_maps["walls"][area.wall_id]
                if area.ceiling_id:
                    clone_ceiling_parent_id = children_id_maps["ceilings"][
                        area.ceiling_id
                    ]
                AreaService.duplicate(
                    base_area=area,
                    clone_room_input_parent_id=clone_room_input.id,
                    clone_wall_parent_id=clone_wall_parent_id,
                    clone_ceiling_parent_id=clone_ceiling_parent_id,
                )
