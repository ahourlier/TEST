from flask import request, g
from flask_accepts import accepts, responds

from app.common.api import AuthenticatedApi
from app.email.emails import api, Email
from app.email.emails.schema import (
    EmailSchema,
    EmailProjectsRecipientsInput,
    EmailProjectsRecipientsOutput,
)
from app.email.emails.service import EmailService


@api.route("/")
class EmailResource(AuthenticatedApi):
    """Send an email"""

    @accepts(schema=EmailSchema, api=api)
    @responds(schema=EmailSchema, api=api)
    def post(self) -> Email:
        """Creates a new email to send"""
        return EmailService.create(request.parsed_obj, user=g.user)


@api.route("/projects/recipients")
class EmailProjectsRecipients(AuthenticatedApi):
    """Helper endpoint to retrieve recipients for one or more projects"""

    @accepts(schema=EmailProjectsRecipientsInput, api=api)
    @responds(schema=EmailProjectsRecipientsOutput, api=api)
    def post(self):
        """Get recipients for a given kind and projects"""
        return dict(
            recipients=EmailService.get_recipients(
                request.parsed_obj["project_ids"], request.parsed_obj["kind"]
            )
        )
