from typing import List
from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.common.services_utils import ServicesUtils
from app.perrenoud.room_inputs.service import RoomInputKinds
from app.perrenoud.rooms import Room
from app.perrenoud.rooms.exceptions import RoomNotFoundException
from app.perrenoud.rooms.interface import RoomInterface
import app.perrenoud.scenarios.service as scenarios_service
import app.perrenoud.heatings.service as heatings_service
import app.perrenoud.areas.service as areas_service
import app.perrenoud.room_inputs.service as rooms_input_service
import app.perrenoud.photos.service as photos_service


class RoomService:
    @staticmethod
    def get_by_id(room_id: str) -> Room:
        db_room = Room.query.get(room_id)
        if db_room is None:
            raise RoomNotFoundException
        return db_room

    @staticmethod
    def create(new_attrs: RoomInterface, scenario_id=None, commit=True) -> Room:
        """Create a new room"""
        inputs_kind = [input_kind.value for input_kind in RoomInputKinds]
        fields_to_remove = inputs_kind.copy()
        fields_to_remove.extend(["heating", "areas"])
        extracted_fields = ServicesUtils.clean_attrs(new_attrs, fields_to_remove)
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        if "heating_id" in new_attrs and new_attrs.get("heating_id"):
            heatings_service.HeatingService.get_by_id((new_attrs.get("heating_id")))
        room = Room(**new_attrs)
        db.session.add(room)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        RoomService.set_room_name(room)
        # Create Areas
        if "areas" in extracted_fields and extracted_fields.get("areas"):
            areas_service.AreaService.create_update_list(
                extracted_fields.get("areas"), room_id=room.id
            )
        # Create room_inputs for each kind
        for input_kind in inputs_kind:
            if input_kind in extracted_fields and extracted_fields.get(input_kind):
                rooms_input_service.RoomInputService.create_update_list(
                    room.id, input_kind, extracted_fields.get(input_kind),
                )

        return room

    @staticmethod
    def set_room_name(room: Room):
        room_index = len(room.scenario.rooms)
        room.update({"name": f"Pièce {room_index}"})

    @staticmethod
    def update(room: Room, changes: RoomInterface, force_update: bool = True) -> Room:
        inputs_kind = [input_kind.value for input_kind in RoomInputKinds]
        fields_to_remove = inputs_kind.copy()
        fields_to_remove.extend(["heating", "areas"])
        extracted_fields = ServicesUtils.clean_attrs(changes, fields_to_remove)
        if "heating_id" in changes and changes.get("heating_id"):
            heatings_service.HeatingService.get_by_id((changes.get("heating_id")))
        if force_update or RoomService.has_changed(room, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != room.id:
                raise InconsistentUpdateIdException()
            initial_name = room.name
            room.update(changes)
            if initial_name != room.name:
                photos_service.PhotoService.rename_photos_room(room)
            # Update Areas
            if "areas" in extracted_fields and extracted_fields.get("areas"):
                areas_service.AreaService.create_update_list(
                    extracted_fields.get("areas"), room_id=room.id
                )
            # Update room_inputs for each kind
            for input_kind in inputs_kind:
                if input_kind in extracted_fields and extracted_fields.get(input_kind):
                    rooms_input_service.RoomInputService.create_update_list(
                        room.id, input_kind, extracted_fields.get(input_kind),
                    )
            db.session.commit()
        return room

    @staticmethod
    def has_changed(room: Room, changes: RoomInterface) -> bool:
        for key, value in changes.items():
            if getattr(room, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(room_id: int) -> int or None:
        room = Room.query.filter(Room.id == room_id).first()
        if not room:
            raise RoomNotFoundException
        db.session.delete(room)
        db.session.commit()
        return room_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_rooms_id = [value.id for value in scenario.rooms]
        changes_rooms_id = [
            rooms_fields["id"] for rooms_fields in changes if "id" in rooms_fields
        ]

        for room_fields in changes:
            # Create
            if "id" not in room_fields:
                RoomService.create(room_fields.copy(), scenario_id)
            # Update
            else:
                room = RoomService.get_by_id(room_fields["id"])
                RoomService.update(room, room_fields.copy())

        # Delete obsolete rooms
        for original_id in original_rooms_id:
            if original_id not in changes_rooms_id:
                RoomService.delete_by_id(original_id)

        return scenario.rooms

    @staticmethod
    def duplicate(base_room, clone_scenario_parent_id, children_id_maps):
        """Duplicate a room and his children"""
        fields_to_treat_separately = ["scenario_id", "heating_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_room, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        base_fields["heating_id"] = children_id_maps["heatings"].get(
            base_room.heating_id
        )
        clone_room = RoomService.create(base_fields, commit=False)
        db.session.flush()
        # Duplicate children
        areas_service.AreaService.duplicate_all_from_room_or_room_input(
            children_id_maps, base_room=base_room, clone_room=clone_room
        )
        rooms_input_service.RoomInputService.duplicate_all_from_room(
            base_room, clone_room, children_id_maps
        )
        db.session.flush()

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario, children_id_maps):
        for room in base_scenario.rooms:
            RoomService.duplicate(room, clone_scenario.id, children_id_maps)
