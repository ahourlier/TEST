import os

from flask import request
import logging

from app import db
from app.common.drive_utils import DriveUtils
from app.common.tasks import create_task
from app.internal_api.base import InternalAPIView
from app.project.projects.service import ProjectService, PROJECT_INIT_QUEUE_NAME


class ProjectInitDriveView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_project = ProjectService.get_by_id(data.get("project_id"))
        if db_project not in ["IN PROGRESS", "DONE"]:
            db_project.drive_init = "IN PROGRESS"
            db.session.commit()
            if db_project.mission.sd_projects_folder_id:
                try:
                    ProjectService.create_drive_structure(db_project)
                except Exception as e:
                    logging.error(e)
                    db_project.drive_init = "ERROR"
                    db.session.commit()
                    raise e
            else:
                logging.warning(
                    f"Mission {db_project.mission.id} Shared Drive not initialized "
                )

            db_project.drive_init = "DONE"
            db.session.commit()

        return "OK"


class ProjectDeleteFilesView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_project = ProjectService.get_by_id(data.get("project_id"))
        if db_project.sd_root_folder_id:
            DriveUtils.delete_file(db_project.sd_root_folder_id)
            logging.info(f"Files from the project {db_project.id} properly deleted ")
            db_project.sd_root_folder_id = None
            db_project.sd_requester_folder_id = None
            db_project.sd_funders_folder_id = None
            db_project.sd_accommodation_pictures_folder_id = None
            db_project.sd_accommodation_report_folder_id = None
            db_project.sd_accommodation_folder_id = None
            db_project.sd_quotes_folder_id = None
            db.session.commit()
            logging.info("Triggering project folder structure recreation")
            create_task(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("QUEUES_LOCATION"),
                queue=PROJECT_INIT_QUEUE_NAME,
                uri=f"{os.getenv('API_URL')}/_internal/projects/init-drive",
                method="POST",
                payload={
                    "project_id": db_project.id,
                },
            )

            return "Success"
        else:
            logging.warning(f"Files from the project {db_project.id} not deleted ")
            return "Fail"
