from flask import g
from flask_sqlalchemy import Pagination
from sqlalchemy.sql.elements import or_

from app import db
from app.auth.users import User
from app.auth.users.model import UserRole
from app.auth.users.service import UserService
from app.common.constants import FRENCH_DATE_FORMAT
from app.project.error_handlers import InconsistentUpdateIdException, ForbiddenException
from app.common.search import sort_query
from app.project.comments import Comment, api
from app.project.comments.error_handlers import CommentNotFoundException
from app.project.comments.interface import CommentInterface
from app.project.projects.model import ProjectStatus
import app.project.projects.service as project_service


DEPOSIT_DATE_UPDATE = "DEPOSIT_DATE_UPDATE"
PAYMENT_DATE_UPDATE = "PAYMENT_DATE_UPDATE"
CERTIFICATION_DATE_UPDATE = "CERTIFICATION_DATE_UPDATE"
EMAIL_SENT = "EMAIL_SENT"
FUNDER_ADVANCE_DATE_UPDATE = "FUNDER_ADVANCE_DATE_UPDATE"
FUNDER_DEPOSIT_DATE_UPDATE = "FUNDER_DEPOSIT_DATE_UPDATE"
FUNDER_PAYMENT_DATE_UPDATE = "FUNDER_PAYMENT_DATE_UPDATE"

BASE_AUTOMATIC_CONTENTS = {
    ProjectStatus.TO_CONTACT.value: "Changement de statut : {Statut}",
    ProjectStatus.CONTACT.value: "Changement de statut : {Statut}",
    ProjectStatus.MEET_ADVICES_TO_PLAN.value: "Changement de statut : {Statut}",
    ProjectStatus.MEET_ADVICES_PLANNED.value: "Changement de statut : {Statut}",
    ProjectStatus.MEET_TO_PROCESS.value: "Changement de statut : {Statut}",
    ProjectStatus.BUILD_ON_GOING.value: "Changement de statut : {Statut}. Retour de visite fait au demandeur",
    ProjectStatus.DEPOSITTED.value: "Changement de statut : {Statut}",
    ProjectStatus.CERTIFIED.value: "Changement de statut : {Statut}",
    ProjectStatus.MEET_CONTROL_TO_PLAN.value: "Changement de statut : {Statut}",
    ProjectStatus.MEET_CONTROL_PLANNED.value: "Changement de statut : {Statut}",
    ProjectStatus.PAYMENT_REQUEST_TO_DO.value: "Changement de statut : {Statut}",
    ProjectStatus.ASKING_FOR_PAY.value: "Changement de statut : {Statut}",
    ProjectStatus.CLEARED.value: "Changement de statut : {Statut}",
    ProjectStatus.DISMISSED.value: "Changement de statut : {Statut}",
    ProjectStatus.NON_ELIGIBLE.value: "Changement de statut : {Statut}",
    DEPOSIT_DATE_UPDATE: "Dépôt du dossier",
    PAYMENT_DATE_UPDATE: "Envoi demande de paiement",
    CERTIFICATION_DATE_UPDATE: "Agrément du dossier",
    EMAIL_SENT: "Envoi d'un mail à {recipients} : {subject}",
    FUNDER_ADVANCE_DATE_UPDATE: "Envoi demande d'avance",
    FUNDER_DEPOSIT_DATE_UPDATE: "Envoi demande d'acompte",
    FUNDER_PAYMENT_DATE_UPDATE: "Paiement effectué",
}

# from main import app

COMMENTS_DEFAULT_PAGE = 1
COMMENTS_DEFAULT_PAGE_SIZE = 100
COMMENTS_DEFAULT_SORT_FIELD = "created_at"
COMMENTS_DEFAULT_SORT_DIRECTION = "desc"


class CommentService:
    @staticmethod
    def get_all(
        page=COMMENTS_DEFAULT_PAGE,
        size=COMMENTS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=COMMENTS_DEFAULT_SORT_FIELD,
        direction=COMMENTS_DEFAULT_SORT_DIRECTION,
        project_id=None,
        author_id=None,
    ) -> Pagination:
        if sort_by == "author_last_name":
            q = (
                Comment.query.join(Comment.author)
                .order_by(
                    User.last_name.asc()
                    if direction == "asc"
                    else User.last_name.desc()
                )
                .order_by(Comment.created_at.desc())
            )
        else:
            q = sort_query(Comment.query, sort_by, direction)

        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Comment.content.ilike(search_term),
                )
            )

        if project_id is not None:
            q = q.filter(Comment.project_id == project_id)
        if author_id is not None:
            q = q.filter(Comment.author_id == author_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(comment_id: str) -> Comment:
        db_comment = Comment.query.get(comment_id)
        if db_comment is None:
            raise CommentNotFoundException()
        return db_comment

    @staticmethod
    def create(new_attrs: CommentInterface) -> Pagination:
        """Create a new comment in a given agency"""
        project_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        new_attrs["author_id"] = g.user.id
        comment = Comment(**new_attrs)
        db.session.add(comment)
        db.session.commit()
        return CommentService.get_all(project_id=comment.project_id)

    @staticmethod
    def update(
        comment: Comment, changes: CommentInterface, force_update: bool = False
    ) -> Pagination:
        """Edit comment if user have sufficient permissions.
        If an admin or an app manager modifies a comment, he/she becames the new author"""

        content_changed = (
            changes.get("content") and changes.get("content") != comment.content
        )
        # If content is modified, user must be the original author (or at least admin or manager)
        if content_changed and comment.author_id != g.user.id:
            if g.user.role != UserRole.ADMIN and g.user.role != UserRole.MANAGER:
                raise ForbiddenException()
            comment.author_id = g.user.id
            del changes["author_id"]

        if force_update or CommentService.has_changed(comment, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != comment.id:
                raise InconsistentUpdateIdException()
            comment.update(changes)
        db.session.commit()
        return CommentService.get_all(project_id=comment.project_id)

    @staticmethod
    def has_changed(comment: Comment, changes: CommentInterface) -> bool:
        for key, value in changes.items():
            if getattr(comment, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(comment_id: int) -> int or None:
        comment = Comment.query.filter(Comment.id == comment_id).first()
        if not comment:
            raise CommentNotFoundException

        # Only the author (or an admin/manager can modify the comment)
        if (
            comment.author_id != g.user.id
            and g.user.role != UserRole.ADMIN
            and g.user.role != UserRole.MANAGER
        ):
            raise ForbiddenException()

        db.session.delete(comment)
        db.session.commit()
        return CommentService.get_all(project_id=comment.project_id)


class AutomaticCommentService:
    @staticmethod
    def automatic_project_status_comment(trigger, project):
        """Create an automatic comment, depending on new project status."""
        base_content = BASE_AUTOMATIC_CONTENTS.get(trigger, None)

        # If new status does not match any corresponding auto comment, do nothing.
        if base_content is not None:
            base_content = base_content.format(Statut=trigger)
        else:
            return

        # In some cases, an extra information (date) must be stored into the comment.
        if (
            trigger == ProjectStatus.MEET_ADVICES_PLANNED.value
            and project.date_advice_meet
        ):
            content = f"{base_content} le {project.date_advice_meet.strftime(FRENCH_DATE_FORMAT)}"
        elif (
            trigger == ProjectStatus.MEET_TO_PROCESS.value and project.date_advice_meet
        ):
            content = f"{base_content}. Visite conseil réalisée le {project.date_advice_meet.strftime(FRENCH_DATE_FORMAT)}"
        elif (
            trigger == ProjectStatus.MEET_CONTROL_PLANNED.value
            and project.date_control_meet
        ):
            content = f"{base_content}. Visite de contrôle réalisée le {project.date_control_meet.strftime(FRENCH_DATE_FORMAT)}"
        else:
            content = base_content

        AutomaticCommentService.create_automatic_comment(content, project)

    @staticmethod
    def automatic_funder_comment(trigger, funder_name, project):
        """Create an automatic comment, depending on new state into simulation."""
        base_content = BASE_AUTOMATIC_CONTENTS.get(trigger, None)
        # If new status does not match any corresponding auto comment, do nothing.
        if base_content is not None:
            base_content = base_content.format(Statut=trigger)
        else:
            return
        content = f"{base_content} {funder_name}"
        AutomaticCommentService.create_automatic_comment(content, project)

    @staticmethod
    def automatic_email_comment(trigger, email, project):
        """
        Create an automatic comment when sending an email
        """
        base_content = BASE_AUTOMATIC_CONTENTS.get(trigger, None)
        if base_content is not None:
            recipients = []
            if email.to:
                recipients.extend(email.to)
            if email.cc:
                recipients.extend(email.cc)
            if email.bcc:
                recipients.extend(email.bcc)

            base_content = base_content.format(
                recipients=", ".join(recipients), subject=email.subject
            )
        else:
            return
        AutomaticCommentService.create_automatic_comment(
            base_content, project, html_content=email.content
        )

    @staticmethod
    def create_automatic_comment(comment_text, project, html_content=None):
        comment = dict(content=comment_text, project_id=project.id, author_id=g.user.id)
        if html_content:
            comment["html_content"] = html_content

        new_comment_fields = CommentInterface(**comment)
        CommentService.create(new_comment_fields)
        api.logger.info(f"New automatic comment saved. Content : {comment_text}")
