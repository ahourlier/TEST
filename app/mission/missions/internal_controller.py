from app.mission.teams.model import UserTeamPositions
import logging
import os

from flask import request, g

from app import db
from app.common.config_error_messages import KEY_SHARED_DRIVE_PERMISSION_EXCEPTION
from app.common.data_import_utils import DataImportUtils
from app.common.drive_utils import DriveUtils
from app.common.exceptions import SharedDriveException, GoogleGroupsException
from app.common.group_utils import GroupUtils
from app.common.tasks import create_task
from app.internal_api.base import InternalAPIView
from app.mission.missions.service import MissionService, MISSION_INIT_QUEUE_NAME


class MissionsInitDriveView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_mission = MissionService.get_by_id(data.get("mission_id"))
        db_mission.drive_init = "IN PROGRESS"
        db.session.commit()
        try:
            MissionService.create_drive_structure(db_mission)
        except Exception as e:
            logging.error(e)
            db_mission.drive_init = "ERROR"
            db.session.commit()
            raise e

        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=MISSION_INIT_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/missions/init-permissions",
            method="POST",
            payload={"mission_id": db_mission.id},
        )

        return "OK"


class MissionInitPermissions(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_mission = MissionService.get_by_id(data.get("mission_id"))

        try:
            MissionService.init_mission_group(db_mission)

            # admins group is organizer
            permission = DriveUtils.insert_permission(
                db_mission.sd_root_folder_id,
                "organizer",
                "group",
                os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP"),
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            # mission creator is organizer
            permission = DriveUtils.insert_permission(
                db_mission.sd_root_folder_id,
                "organizer",
                "user",
                db_mission.creator,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            permission = DriveUtils.insert_permission(
                db_mission.sd_root_folder_id,
                "fileOrganizer",
                "group",
                f"{os.getenv('GROUP_EMAIL_ENV_PREFIX', '')}oslo-mission-{db_mission.code_name}@{os.getenv('GSUITE_DOMAIN')}",
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)
        except Exception as e:
            logging.error(e)
            db_mission.drive_init = "ERROR"
            db.session.commit()
            raise e

        db_mission.drive_init = "DONE"
        db.session.commit()

        for db_project in db_mission.projects:
            if db_project.drive_init not in ["IN PROGRESS", "DONE"]:
                if (
                    db_project.sd_root_folder_id
                    and db_project.sd_quotes_folder_id
                    and db_project.sd_accommodation_folder_id
                    and db_project.sd_accommodation_report_folder_id
                    and db_project.sd_accommodation_pictures_folder_id
                    and db_project.sd_funders_folder_id
                    and db_project.sd_requester_folder_id
                ):
                    db_project.drive_init = "DONE"
                    db.session.commit()
                else:
                    db_project.drive_init = "IN PROGRESS"
                    db.session.commit()
                    create_task(
                        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                        location=os.getenv("QUEUES_LOCATION"),
                        queue="project-queue",
                        uri=f"{os.getenv('API_URL')}/_internal/projects/init-drive",
                        method="POST",
                        payload={
                            "project_id": db_project.id,
                        },
                    )

        return "OK"


class MissionComputePermissions(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_mission = MissionService.get_by_id(data.get("mission_id"))
        if not db_mission.google_group_id:
            if not data.get("update", True):
                # create_task(
                #     project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                #     location=os.getenv("QUEUES_LOCATION"),
                #     queue=MISSION_INIT_QUEUE_NAME,
                #     uri=f"{os.getenv('API_URL')}/_internal/missions/compute-permissions",
                #     method="POST",
                #     payload={"mission_id": db_mission.id, "update": False},
                # )
                return "OK"
            else:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)
        current_members = GroupUtils.list_members(db_mission.google_group_id)
        if current_members is not None:
            members_emails = [m.get("email") for m in current_members]
            to_add = []
            for t in db_mission.teams:
                if t.user:
                    if t.user.email not in members_emails:
                        to_add.append(t.user.email)
                    else:
                        members_emails.remove(t.user.email)
                elif t.antenna:
                    if t.antenna.email_address not in members_emails:
                        to_add.append(t.antenna.email_address)
                    else:
                        members_emails.remove(t.antenna.email_address)
                elif t.agency:
                    if t.agency.email_address not in members_emails:
                        to_add.append(t.agency.email_address)
                    else:
                        members_emails.remove(t.agency.email_address)

            for member_to_add in to_add:
                create_task(
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("QUEUES_LOCATION"),
                    queue=MISSION_INIT_QUEUE_NAME,
                    uri=f"{os.getenv('API_URL')}/_internal/missions/add-member",
                    method="POST",
                    payload={
                        "group_id": db_mission.google_group_id,
                        "member_email": member_to_add,
                    },
                )

            for member_to_delete in members_emails:
                create_task(
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("QUEUES_LOCATION"),
                    queue=MISSION_INIT_QUEUE_NAME,
                    uri=f"{os.getenv('API_URL')}/_internal/missions/remove-member",
                    method="POST",
                    payload={
                        "group_id": db_mission.google_group_id,
                        "member_email": member_to_delete,
                    },
                )

        return "OK"


class MissionAddMember(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        resp = GroupUtils.add_member(data.get("member_email"), data.get("group_id"))

        if not resp:
            raise GoogleGroupsException

        return "OK"


class MissionRemoveMember(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        resp = GroupUtils.remove_member(data.get("member_email"), data.get("group_id"))

        if not resp:
            raise GoogleGroupsException

        return "OK"
