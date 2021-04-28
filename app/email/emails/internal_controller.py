import logging
from flask import request

from app.email.emails.model import EmailStatus
from app.internal_api.base import InternalAPIView
from app.email.emails.service import EmailService


class EmailSendView(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_email = EmailService.get_by_id(data.get("emailId"))
        if db_email.status == EmailStatus.TO_SEND.value:
            EmailService.send_email(db_email)
        else:
            logging.warning(f"Email {db_email.id} has already been sent.")

        return "OK"
