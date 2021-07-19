import base64
import io
import logging
import os
from datetime import datetime
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from flask import request
from googleapiclient import errors
from googleapiclient.http import MediaIoBaseUpload
from html2text import html2text

from app import db
from app.auth.users import User
from app.auth.users.model import UserKind
from app.common.drive_utils import DriveUtils
from app.common.gmail_utils import GmailUtils
from app.common.google_apis import GMailService, DriveService
from app.common.tasks import create_task
from app.email.emails import Email
from app.email.emails.error_handlers import (
    EmailNotFoundException,
    EmailMissingRecipientException,
    EmailNotInternalSenderException,
)
from app.email.emails.model import EmailStatus
from app.email.emails.schema import RECIPIENT_REFERRER_KIND, RECIPIENT_REQUESTER_KIND
from app.project.comments.service import (
    AutomaticCommentService,
    EMAIL_SENT,
)
from app.project.projects import Project
from app.project.projects.error_handlers import ProjectNotFoundException
from app.project.projects.service import ProjectService

EMAILS_QUEUE_NAME = "emails-queue"


class EmailService:
    @staticmethod
    def get_by_id(email_id: int) -> Email:
        db_email = Email.query.get(email_id)
        if not db_email:
            raise EmailNotFoundException
        return db_email

    @staticmethod
    def create(new_attrs: dict, user: User) -> Email:
        """ Create a new email to be sent """

        if user.kind != UserKind.EMPLOYEE:
            raise EmailNotInternalSenderException

        has_recipients = False
        if "to" in new_attrs:
            if len(new_attrs["to"]) > 0:
                has_recipients = True
        if "cc" in new_attrs:
            if len(new_attrs["cc"]) > 0:
                has_recipients = True
        if "bcc" in new_attrs:
            if len(new_attrs["bcc"]) > 0:
                has_recipients = True

        if not has_recipients:
            raise EmailMissingRecipientException

        new_attrs["sender_id"] = user.id

        if "project_ids" in new_attrs and new_attrs["project_ids"]:
            projects_dict = {}
            db_projects = Project.query.filter(
                Project.id.in_(new_attrs["project_ids"])
            ).all()
            for db_project in db_projects:
                projects_dict[db_project.id] = db_project
            does_not_exist = any(
                project_id not in projects_dict.keys()
                for project_id in new_attrs["project_ids"]
            )
            if does_not_exist:
                raise ProjectNotFoundException

        email = Email(**new_attrs)
        db.session.add(email)
        db.session.commit()

        if email.project_ids:
            list(
                map(
                    lambda x: AutomaticCommentService.automatic_email_comment(
                        EMAIL_SENT, email, project=projects_dict[x]
                    ),
                    email.project_ids,
                )
            )

        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=EMAILS_QUEUE_NAME,
            uri=f"{request.host_url}api/_internal/emails/send",
            method="POST",
            payload={"emailId": email.id},
        )

        return email

    @staticmethod
    def send_email(db_email: Email):
        content = db_email.content.encode().decode("utf-8")
        subject = db_email.subject
        sender = db_email.sender.email
        to = ",".join(db_email.to)
        cc = None
        bcc = None
        if db_email.cc:
            cc = ",".join(db_email.cc)
        if db_email.bcc:
            bcc = ",".join(db_email.bcc)

        files = []
        drive_service = DriveService(user_email=db_email.sender.email).get()
        for attachment_id in db_email.attachments:
            attachment_file, name, mime_type = DriveUtils.download_file(
                attachment_id, db_email.sender.email, drive_service
            )
            if attachment_file is not None:
                files.append((attachment_file, name, mime_type))

        message = GmailUtils.create_message_with_attachment(
            sender, to, subject, content, files, cc=cc, bcc=bcc
        )
        try:
            GmailUtils.send_message(message, db_email.sender.email)
            db_email.sent_date = datetime.now()
            db_email.status = EmailStatus.SENT.value
            print("success sending mail")
            db.session.commit()

        except errors.HttpError as e:
            logging.error(f"Unable to send email with id {db_email.id} : {e}")
            db_email.status = EmailStatus.ERROR.value
            db.session.commit()
            raise e

    @staticmethod
    def get_recipients(project_ids: List[int], kind: str) -> List[str]:
        db_projects = ProjectService.get_projects(project_ids, raise_error=True)
        recipients = []
        for db_project in db_projects:
            if kind == RECIPIENT_REFERRER_KIND:
                recipients.extend([r.email for r in db_project.referrers])
            elif kind == RECIPIENT_REQUESTER_KIND:
                requester_email = None
                for contact in db_project.requester.contacts:
                    if contact.main_contact:
                        requester_email = contact.email
                        break
                if not requester_email:
                    requester_email = db_project.requester.email
                if requester_email is not None:
                    recipients.append(requester_email)

        return list(set(recipients))
