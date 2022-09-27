from enum import Enum
import os
from app.common.config_error_messages import KEY_SHARED_DRIVE_COPY_EXCEPTION
from app.common.drive_utils import DRIVE_DEFAULT_FIELDS, DriveUtils
from app.common.exceptions import SharedDriveException
from app.common.tasks import create_task
from app.copro.copros.service import CoproService
from app.dam.documents.error_handlers import shared_drive_exception

from flask import jsonify
from app.dam.documents.service import DOC_EDIT_QUEUE_NAME

from app.mission.missions.model import Mission
from app.mission.missions.service import MissionService


class DocumentV2Sources(Enum):
    MARKET = "MARKET"
    COPRO = "COPRO"
    THEMATIC = "THEMATIC"


class DocumentGenerationV2Service:
    @staticmethod
    def generate_document(
        template_id: int,
        source: str,
        user_email: str,
        mission_id: int,
        copro_folder_id: int,
        thematic_folder_id: int,
    ):
        mission = MissionService.get_by_id(mission_id)
        template = DriveUtils.get_file(template_id, user_email=user_email)
        if template is not None:
            name = f'{template.get("name")} - Mission/{mission.code_name}'
        else:
            resp, code = shared_drive_exception(SharedDriveException())
            resp.code = code
            return jsonify(resp)

        # Controller schema forces id to exist
        if source == DocumentV2Sources.MARKET.value:
            dest_folder = mission.sdv2_donnees_sortie_folder
        elif source == DocumentV2Sources.COPRO.value:
            dest_folder = copro_folder_id
        elif source == DocumentV2Sources.THEMATIC.value:
            dest_folder = thematic_folder_id

        # properties = {
        #     "missionId": mission.mission_id,
        #     "kind": source,
        # }
        if dest_folder is not None:
            resp = DriveUtils.copy_file(
                template_id,
                dest_folder,
                name=name,
                # properties=properties,
                user_email=user_email,
                fields=DRIVE_DEFAULT_FIELDS,
            )
            if not resp:
                raise SharedDriveException(KEY_SHARED_DRIVE_COPY_EXCEPTION)

            # create_task(
            #     project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            #     location=os.getenv("QUEUES_LOCATION"),
            #     queue=DOC_EDIT_QUEUE_NAME,
            #     uri=f"{os.getenv('API_URL')}/_internal/documents/edit",
            #     method="POST",
            #     payload={"user_email": user_email},
            # )
