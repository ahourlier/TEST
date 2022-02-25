from app import db
from flask import request
from app.common.config_error_messages import KEY_SHARED_DRIVE_PERMISSION_EXCEPTION
from app.common.drive_utils import DriveUtils
from app.common.tasks import create_task
from app.internal_api.base import InternalAPIView
from app.mission.missions.service import MissionService


class ImportRunView(InternalAPIView):
    def put(self):
        payload = request.get_json(force=True)
        print()
