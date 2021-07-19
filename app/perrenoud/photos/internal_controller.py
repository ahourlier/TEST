import os

from flask import request

from app.common.tasks import create_task
from app.internal_api.base import InternalAPIView
import app.perrenoud.photos.service as photos_service

RENAME_PHOTO_QUEUE_NAME = "rename-photo-room-queue"


class RenamePhotosRoomView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        files = photos_service.PhotoService.fetch_photos(
            {"project_id": data.get("project_id"), "room_id": data.get("room_id"),},
            email_user=data.get("email_user"),
        )
        for file in files:
            root_name = file.get("appProperties").get("root_name")
            photo_id = file.get("drive_id")
            create_task(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("QUEUES_LOCATION"),
                queue=RENAME_PHOTO_QUEUE_NAME,
                uri=f"{request.host_url}api/_internal/rename_photos/single",
                method="POST",
                payload={
                    "room_id": data.get("room_id"),
                    "id": photo_id,
                    "root_name": root_name,
                    "user_email": data.get("email_user"),
                },
            )

        return "OK"


class RenamePhotoRoomView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)

        photos_service.PhotoService.rename_photo_room(
            data.get("room_id"),
            data.get("id"),
            data.get("root_name"),
            data.get("user_email"),
        )
        return "Ok"
