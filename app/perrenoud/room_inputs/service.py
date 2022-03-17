from enum import Enum
from typing import List
from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
from app.common.services_utils import ServicesUtils
from app.perrenoud import RoomInput
from app.perrenoud.room_inputs.error_handlers import (
    RoomInputNotFoundException,
    TypeRoomInputInUseException,
)
from app.perrenoud.room_inputs.interface import RoomInputInterface
import app.perrenoud.areas.service as areas_service
import app.perrenoud.rooms.service as rooms_service


class RoomInputKinds(Enum):
    WALL = "wall_inputs"
    WOODWORK = "woodwork_inputs"
    CEILING = "ceiling_inputs"
    FLOOR = "floor_inputs"


class RoomInputService:
    @staticmethod
    def get_by_id(room_input_id: str) -> RoomInput:
        db_room_input = RoomInput.query.get(room_input_id)
        if db_room_input is None:
            raise RoomInputNotFoundException
        return db_room_input

    @staticmethod
    def create(
        new_attrs: RoomInputInterface, kind, room_id=None, commit=True
    ) -> RoomInput:
        """Create a new room_input"""
        inputs_kind = [input_kind.value for input_kind in RoomInputKinds]
        fields_to_remove = inputs_kind.copy()
        fields_to_remove.extend(["heating", "areas"])
        extracted_fields = ServicesUtils.clean_attrs(new_attrs, fields_to_remove,)
        if room_id is not None:
            new_attrs["room_id"] = room_id
        rooms_service.RoomService.get_by_id(new_attrs.get("room_id"))
        new_attrs["kind"] = kind
        if RoomInputService.is_type_forbidden(new_attrs):
            raise TypeRoomInputInUseException()
        room_input = RoomInput(**new_attrs)
        db.session.add(room_input)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        if "areas" in extracted_fields and extracted_fields.get("areas"):
            areas_service.AreaService.create_update_list(
                extracted_fields.get("areas"), room_input_id=room_input.id
            )
        return room_input

    @staticmethod
    def update(
        room_input: RoomInput, changes: RoomInputInterface, force_update: bool = True
    ) -> RoomInput:
        if force_update or RoomInputService.has_changed(room_input, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != room_input.id:
                raise InconsistentUpdateIdException()
            inputs_kind = [input_kind.value for input_kind in RoomInputKinds]
            fields_to_remove = inputs_kind.copy()
            fields_to_remove.extend(["heating", "areas"])
            extracted_fields = ServicesUtils.clean_attrs(changes, fields_to_remove,)
            if RoomInputService.is_type_forbidden(changes, room_input):
                raise TypeRoomInputInUseException()
            room_input.update(changes)
            db.session.commit()
            areas_service.AreaService.create_update_list(
                extracted_fields.get("areas"), room_input_id=room_input.id
            )
        return room_input

    @staticmethod
    def is_type_forbidden(attrs: RoomInputInterface, room_input: RoomInput = None):
        parent_room = rooms_service.RoomService.get_by_id((attrs.get("room_id")))
        if (
            RoomInputService.type_already_in_use(
                attrs, room_input, parent_room, "wall_id"
            )
            or RoomInputService.type_already_in_use(
                attrs, room_input, parent_room, "woodwork_id"
            )
            or RoomInputService.type_already_in_use(
                attrs, room_input, parent_room, "ceiling_id"
            )
            or RoomInputService.type_already_in_use(
                attrs, room_input, parent_room, "floor_id"
            )
        ):
            return True
        return False

    @staticmethod
    def type_already_in_use(attrs, room_input, parent_room, field_id_name: str):
        if room_input and attrs.get(field_id_name) == getattr(
            room_input, field_id_name
        ):
            return False
        if field_id_name in attrs and attrs.get(field_id_name):
            parent_linked_id = [
                getattr(input, field_id_name) for input in parent_room.inputs
            ]
            result = attrs.get(field_id_name) in parent_linked_id
            return result

    @staticmethod
    def has_changed(room_input: RoomInput, changes: RoomInputInterface) -> bool:
        for key, value in changes.items():
            if getattr(room_input, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(room_input_id: int) -> int or None:
        room_input = RoomInput.query.filter(RoomInput.id == room_input_id).first()
        if not room_input:
            raise RoomInputNotFoundException
        db.session.delete(room_input)
        db.session.commit()
        return room_input_id

    @staticmethod
    def create_update_list(room_id, kind, changes: List):
        room = rooms_service.RoomService.get_by_id(room_id)
        original_room_inputs_id = [
            room_input.id for room_input in room.inputs if room_input.kind == kind
        ]
        changes_room_inputs_id = [
            room_inputs_fields["id"]
            for room_inputs_fields in changes
            if "id" in room_inputs_fields
        ]

        for room_input_fields in changes:
            # Create
            if "id" not in room_input_fields:
                RoomInputService.create(room_input_fields.copy(), kind, room.id)
            # Update
            else:
                room_input = RoomInputService.get_by_id(room_input_fields["id"])
                RoomInputService.update(room_input, room_input_fields.copy())

        # Delete obsolete room_inputs
        for original_id in original_room_inputs_id:
            if original_id not in changes_room_inputs_id:
                RoomInputService.delete_by_id(original_id)

        return room.inputs

    @staticmethod
    def duplicate(
        base_room_input,
        clone_room_parent_id,
        kind,
        children_id_maps,
        clone_wall_parent_id=None,
        clone_woodwork_parent_id=None,
        clone_ceiling_parent_id=None,
        clone_floor_parent_id=None,
    ):
        """Duplicate a room_input, based on provided cloned parents id"""
        fields_to_treat_separately = [
            "room_id",
            "wall_id",
            "woodwork_id",
            "ceiling_id",
            "floor_id",
        ]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_room_input, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["room_id"] = clone_room_parent_id
        base_fields["wall_id"] = clone_wall_parent_id
        base_fields["woodwork_id"] = clone_woodwork_parent_id
        base_fields["ceiling_id"] = clone_ceiling_parent_id
        base_fields["floor_id"] = clone_floor_parent_id

        clone_room_input = RoomInputService.create(base_fields, kind, commit=False)
        db.session.flush()
        # Duplicate areas
        areas_service.AreaService.duplicate_all_from_room_or_room_input(
            children_id_maps,
            base_room_input=base_room_input,
            clone_room_input=clone_room_input,
        )
        return clone_room_input

    @staticmethod
    def duplicate_all_from_room(base_room, clone_room, children_id_maps):
        """Duplicate all rooms_input within a base_room"""
        for room_input in base_room.inputs:
            clone_wall_parent_id = None
            clone_woodwork_parent_id = None
            clone_ceiling_parent_id = None
            clone_floor_parent_id = None
            if room_input.wall_id:
                clone_wall_parent_id = children_id_maps["walls"][room_input.wall_id]
            if room_input.woodwork_id:
                clone_woodwork_parent_id = children_id_maps["woodworks"][
                    room_input.woodwork_id
                ]
            if room_input.ceiling_id:
                clone_ceiling_parent_id = children_id_maps["ceilings"][
                    room_input.ceiling_id
                ]
            if room_input.floor_id:
                clone_floor_parent_id = children_id_maps["floors"][room_input.floor_id]
            RoomInputService.duplicate(
                room_input,
                clone_room.id,
                room_input.kind,
                children_id_maps,
                clone_wall_parent_id=clone_wall_parent_id,
                clone_woodwork_parent_id=clone_woodwork_parent_id,
                clone_ceiling_parent_id=clone_ceiling_parent_id,
                clone_floor_parent_id=clone_floor_parent_id,
            )
