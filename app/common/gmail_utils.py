import base64
import logging
import mimetypes
import os
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient import errors

from app.common.google_apis import GMailService


class GmailUtils:
    # TODO rendre tout ça générique. if file is None, if cc or bcc are none etc.
    @staticmethod
    def create_message_with_attachment(
        sender, to, subject, message_text, files=None, cc=None, bcc=None
    ):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
          file: The path to the file to be attached.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message["to"] = to
        message["from"] = sender
        if subject:
            message["subject"] = subject
        if cc:
            message["Cc"] = cc
        if bcc:
            message["Bcc"] = bcc

        msg = MIMEText(message_text, "html")
        message.attach(msg)

        if not isinstance(files, list):
            files = [files]
        for file, filename, content_type in files:
            main_type, sub_type = content_type.split("/", 1)

            if main_type == "text":
                msg = MIMEText(file.read(), _subtype=sub_type)
            elif main_type == "image":
                msg = MIMEImage(file.read(), _subtype=sub_type)
            elif main_type == "audio":
                msg = MIMEAudio(file.read(), _subtype=sub_type)
            else:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())
            file.close()
            encoders.encode_base64(msg)

            msg.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(msg)

        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    @staticmethod
    def send_message(
        message,
        user_email,
    ):
        """Send an email message.

        Args:
        user_id: User's email address. The default value "me"
        indicates the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        service = GMailService(user_email).get()
        try:
            message = (
                service.users().messages().send(userId="me", body=message).execute()
            )
            return message
        except errors.HttpError as e:
            raise e
