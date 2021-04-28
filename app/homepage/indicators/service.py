from flask import g

from app.common.exceptions import InvalidSearchFieldException
from app.project.projects import Project
import app.project.projects.service as projects_service
from app.project.projects.model import ProjectStatus


class IndicatorService:
    @staticmethod
    def get(missions_id=None, requester_type=None):
        authorized_types = ["PO", "PB"]
        data = []
        status_filtered = [
            ProjectStatus.BUILD_ON_GOING.value,
            ProjectStatus.DEPOSITTED.value,
            ProjectStatus.CERTIFIED.value,
            ProjectStatus.CLEARED.value,
        ]
        labels = ["En cours de montage", "Déposés", "Agréés", "Soldés"]

        if requester_type is not None and requester_type not in authorized_types:
            raise InvalidSearchFieldException()
        base_q = projects_service.ProjectService.filter_query_project(
            user=g.user,
            q=Project.query,
            missions_id=missions_id,
            requester_type=requester_type,
        )

        for status in status_filtered:
            count = projects_service.ProjectService.filter_query_project(
                user=g.user, q=base_q, project_status=status
            ).count()
            data.append(count)

        return {"labels": labels, "datasets": [{"data": data}]}
