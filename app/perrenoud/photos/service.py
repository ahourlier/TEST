import os
from enum import Enum

import mimetypes
from flask import g, request
import app.project.accommodations.service as accommodations_service
import app.perrenoud.rooms.service as rooms_service
import app.perrenoud.scenarios.service as scenarios_service
from werkzeug.utils import secure_filename
from app.common.config_error_messages import (
    KEY_SHARED_DRIVE_COPY_EXCEPTION,
    KEY_SHARED_DRIVE_FETCH_EXCEPTION,
)
from app.common.drive_utils import DriveUtils, DRIVE_DEFAULT_FIELDS
from app.common.exceptions import SharedDriveException, InvalidFileException
from app.common.tasks import create_task
from app.common.upload_utils import UploadUtils
from app.perrenoud.photos.exceptions import (
    MissingSectionException,
    InvalidPhotoContextException,
)
import app.project.projects.service as projects_service

RENAME_PHOTOS_QUEUE_NAME = "rename-photos-room-queue"
AUTHORIZED_PHOTOS_EXTENSION = ["png", "jpg", "jpeg"]
MAX_UPLOAD_SIZE = 5000000


SECTIONS = ["general", "room", "common_area", "equipment"]


class PhotoService:
    @staticmethod
    def add_multiple_photos(
        project_id,
        files,
        section,
        accommodation_id=None,
        room_id=None,
        scenario_id=None,
    ):
        """Add multiple photos from the user drive into accommodations/photos folder.
        Insert the appropriate photo monitoring entity into base"""
        project = projects_service.ProjectService.get_by_id(project_id)
        if section not in SECTIONS:
            raise MissingSectionException()
        dest_folder = project.sd_accommodation_pictures_folder_id
        accommodation = None
        if accommodation_id:
            accommodation = accommodations_service.AccommodationService.get_by_id(
                accommodation_id
            )
        room = None
        if room_id:
            room = rooms_service.RoomService.get_by_id(room_id)
        scenario = None
        if scenario_id:
            scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)

        response = []
        for file in files:
            photo_name = file.get("filename")
            photo_id = file.get("id")
            response.append(
                PhotoService.add_photo(
                    project,
                    dest_folder,
                    photo_id,
                    photo_name,
                    section,
                    accommodation=accommodation,
                    room=room,
                    scenario=scenario,
                )
            )

        return response

    @staticmethod
    def add_photo(
        project,
        dest_folder,
        photo_id,
        photo_name,
        section,
        accommodation=None,
        room=None,
        scenario=None,
    ):
        """Add a photo from the user drive into accommodations/photos folder
        Insert the appropriate photo monitoring entity into base"""
        prefix = PhotoService.build_prefix(
            project, section, accommodation=accommodation, room=room
        )
        properties = {
            "projectId": project.id,
            "section": section,
            "root_name": photo_name,
        }
        if room:
            properties["roomId"] = room.id
        if accommodation:
            properties["accommodationId"] = accommodation.id
        if scenario:
            properties["scenarioId"] = scenario.id

        resp = DriveUtils.copy_file(
            photo_id,
            parent_id=dest_folder,
            name=f"{prefix}{photo_name}",
            properties=properties,
            user_email=g.user.email,
            fields=DRIVE_DEFAULT_FIELDS,
        )

        # On photoUpload, importing local files, we must delete the original file
        # to avoid a copy with wrong name
        source_file = DriveUtils.get_file(file_id=photo_id, fields="parents")
        if source_file:
            if dest_folder in source_file.get("parents", []):
                DriveUtils.delete_file(file_id=photo_id, user_email=g.user.email)

        if not resp:
            raise SharedDriveException(KEY_SHARED_DRIVE_COPY_EXCEPTION)

        return {
            "name": f"{prefix}{photo_name}",
            "drive_id": resp.get("id"),
            "url": f"https://drive.google.com/uc?id={resp.get('id')}",
        }

    @staticmethod
    def upload_multiple(
        project_id, accommodation_id, photos, section, room_id=None, scenario_id=None
    ):
        """Upload multiple photos from user device"""
        if section not in SECTIONS:
            raise MissingSectionException()
        project = projects_service.ProjectService.get_by_id(project_id)
        accommodation = None
        if accommodation_id:
            accommodation = accommodations_service.AccommodationService.get_by_id(
                accommodation_id
            )
        room = None
        if room_id:
            room = rooms_service.RoomService.get_by_id(room_id)
        scenario = None
        if scenario_id:
            scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        created_photos = []
        for photo in photos:
            new_photo = PhotoService.upload(
                project,
                photo,
                section,
                accommodation=accommodation,
                room=room,
                scenario=scenario,
            )
            created_photos.append(new_photo)
        return created_photos

    @staticmethod
    def upload(project, photo, section, accommodation=None, room=None, scenario=None):
        """Upload a photo from user device"""

        properties = {
            "projectId": project.id,
            "section": section,
        }
        if accommodation:
            properties["accommodationId"] = accommodation.id
        if room:
            properties["roomId"] = room.id
        if scenario:
            properties["scenarioId"] = scenario.id
        if not UploadUtils.is_valid_file(
            photo, AUTHORIZED_PHOTOS_EXTENSION, MAX_UPLOAD_SIZE
        ):
            raise InvalidFileException()
        prefix = PhotoService.build_prefix(
            project, section, accommodation=accommodation, room=room
        )
        photo_name = secure_filename(photo.filename)
        properties["root_name"] = photo_name
        photo_name = f"{prefix}{photo_name}"
        mimetype = mimetypes.guess_type(photo.filename)[0]

        uploaded_photo = DriveUtils.upload_file(
            g.user.email,
            photo,
            photo_name,
            mimetype,
            project.sd_accommodation_pictures_folder_id,
            properties=properties,
        )
        return {
            "name": photo_name,
            "drive_id": uploaded_photo.get("id"),
            "url": f"https://drive.google.com/uc?id={uploaded_photo.get('id')}",
        }

    @staticmethod
    def build_prefix(project, section, accommodation=None, room=None):
        is_PB = project.requester.type == "PB"
        if section == "room":
            try:
                return (
                    f"{accommodation.name}_{room.name}_" if is_PB else f"{room.name}_"
                )
            except:
                InvalidPhotoContextException()
        if section == "general":
            try:
                return (
                    f"{accommodation.name}_Vue_générale_" if is_PB else f"Vue_générale_"
                )
            except:
                InvalidPhotoContextException()
        if section == "equipment":
            try:
                equipments_photos = PhotoService.fetch_photos(
                    {
                        "project_id": project.id,
                        "section": "equipment",
                        "accommodation_id": accommodation.id,
                    }
                )
                number_photo = len(equipments_photos) + 1
                return (
                    f"{accommodation.name}_Equipement_{number_photo}_"
                    if is_PB
                    else f"Equipement_{number_photo}_"
                )
            except:
                InvalidPhotoContextException()
        if section == "common_area":
            return f"Parties_communes_"

        return "_"

    @staticmethod
    def fetch_photos(request, email_user=None):
        if not email_user:
            email_user = g.user.email
        project = projects_service.ProjectService.get_by_id(request.get("project_id"))
        app_properties = {}
        if "section" in request and request.get("section"):
            app_properties["section"] = request.get("section")
        if "accommodation_id" in request and request.get("accommodation_id"):
            app_properties["accommodationId"] = request.get("accommodation_id")
        if "room_id" in request and request.get("room_id"):
            app_properties["roomId"] = request.get("room_id")
        files = DriveUtils.list_files(
            app_properties,
            project.sd_accommodation_pictures_folder_id,
            user_email=email_user,
        )
        if files is None:
            return []
        return [
            {
                "drive_id": file.get("id"),
                "name": file.get("name"),
                "url": f"https://drive.google.com/uc?id={file.get('id')}",
                "appProperties": file.get("appProperties"),
            }
            for file in files
        ]

    @staticmethod
    def rename_photos_room(room):
        """Rename all photos linked to the room with the current room name"""
        project = room.scenario.accommodation.project
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=RENAME_PHOTOS_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/rename_photos/multiple",
            method="POST",
            payload={
                "project_id": project.id,
                "room_id": room.id,
                "email_user": g.user.email,
            },
        )

    @staticmethod
    def rename_photo_room(room_id, photo_id, root_name, user_email):
        """Rename a photo from the new parent room name"""
        room = rooms_service.RoomService.get_by_id(room_id)
        new_prefix = PhotoService.build_prefix(
            room.scenario.accommodation.project,
            "room",
            room=room,
            accommodation=room.scenario.accommodation,
        )
        new_name = f"{new_prefix}{root_name}"
        DriveUtils.update_file(photo_id, dict(name=new_name), user_email=user_email)
        return "Photo updated"
