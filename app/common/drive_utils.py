import io
import logging
import os
from uuid import uuid4

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload, MediaFileUpload

from app.common.google_apis import DriveService

DRIVE_DEFAULT_FIELDS = "kind,id,name,mimeType,webViewLink,iconLink,modifiedTime,driveId"

GOOGLE_DOCS_MIMETYPE = "application/vnd.google-apps.document"
GOOGLE_SHEETS_MIMETYPE = "application/vnd.google-apps.spreadsheet"
GOOGLE_SLIDES_MIMETYPE = "application/vnd.google-apps.presentation"

GOOGLE_DRIVE_MIMETYPES = [
    GOOGLE_DOCS_MIMETYPE,
    GOOGLE_SHEETS_MIMETYPE,
    GOOGLE_SLIDES_MIMETYPE,
]


class DriveUtils:
    @staticmethod
    def create_shared_drive(
        name, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """Creates a shared drive using provided name and user_email"""
        if not client:
            client = DriveService(user_email).get()
        try:
            uid = str(uuid4())
            resp = (
                client.drives()
                .create(requestId=uid, body=dict(name=name))
                .execute(num_retries=3)
            )
            return resp.get("id")
        except HttpError as e:
            logging.error(f"Unable to create shared drive with name {name}: {e}")
            return None

    @staticmethod
    def create_folder(
        name,
        parent_id,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        batch=False,
    ):
        """Creates a folder using provided name and user_email in the parent_id"""
        if not client:
            client = DriveService(user_email).get()
        try:
            folder_data = {
                "name": name,
                "parents": [parent_id],
                "mimeType": "application/vnd.google-apps.folder",
            }
            request = client.files().create(
                body=folder_data, fields="id", supportsAllDrives=True
            )
            if not batch:
                resp = request.execute(num_retries=3)
                return resp.get("id")
            else:
                return request

        except HttpError as e:
            logging.error(f"Unable to create folder {name} in parent {parent_id}: {e}")
            return None

    @staticmethod
    def insert_permission(
        file_id,
        role,
        type,
        email,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
    ):
        """
        Add a permission to a google drive file or folder
        :param file_id: drive id of the file or folder on which to add permission
        :param role: role of the permission (owner, organizer, fileOrganizer, writer, commenter, reader)
        :param type: type of the permission (user or group) / does not support domain or anyone
        :param email: email of the user or group for the permission
        """

        if not client:
            client = DriveService(user_email).get()
        try:
            resp = (
                client.permissions()
                .create(
                    fileId=file_id,
                    sendNotificationEmail=False,
                    supportsAllDrives=True,
                    body=dict(role=role, type=type, emailAddress=email),
                )
                .execute(num_retries=3)
            )
            return resp.get("id")
        except HttpError as e:
            logging.error(
                f"Unable to add permission for {email} to file/folder {file_id}: {e}"
            )
            return None

    @staticmethod
    def rename_shared_drive(
        sd_id, name, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """Rename shared drive sd_id with provided name"""
        if not client:
            client = DriveService(user_email).get()
        try:
            (
                client.drives()
                .update(driveId=sd_id, body=dict(name=name))
                .execute(num_retries=3)
            )
            return True
        except HttpError as e:
            logging.error(
                f"Unable to rename shared drive {sd_id} with name {name}: {e}"
            )
            return None

    @staticmethod
    def copy_file(
        file_id,
        parent_id=None,
        name=None,
        properties=None,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        fields="id",
    ):
        """Copy a file to the destination folder"""
        if not client:
            client = DriveService(user_email).get()
        try:
            file_data = {}
            if parent_id is not None:
                file_data["parents"] = [parent_id]
            if name is not None:
                file_data["name"] = name
            else:
                data = DriveUtils.get_file(
                    file_id, fields="name", user_email=user_email
                )
                if data is not None:
                    file_data["name"] = data.get("name")
            if properties is not None:
                file_data["appProperties"] = properties

            resp = (
                client.files()
                .copy(
                    fileId=file_id,
                    supportsAllDrives=True,
                    body=file_data,
                    fields=fields,
                )
                .execute(num_retries=3)
            )
            if fields is "id":
                return resp.get("id")
            else:
                return resp
        except HttpError as e:
            logging.error(f"Unable to copy file {file_id} to parent {parent_id}: {e}")
            return None

    @staticmethod
    def get_file(
        file_id,
        fields=None,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
    ):
        """Get a file"""
        if not client:
            client = DriveService(user_email).get()
        try:
            resp = (
                client.files()
                .get(fileId=file_id, supportsAllDrives=True, fields=fields)
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to get file {file_id}: {e}")
            return None

    @staticmethod
    def list_files(
        app_properties,
        parent_folder,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
    ):
        """List files"""
        if not client:
            client = DriveService(user_email).get()

        conditions = []
        i = 0
        q = f"trashed = false and ('{parent_folder}' in parents)"
        for key, value in app_properties.items():
            if i == 0:
                q += " and "
            q += (
                "(appProperties has {key = '"
                + key
                + "' and value = '"
                + str(value)
                + "'})"
            )
            q += " and "
            i += 1
        q = q[:-5]
        try:
            resp = (
                client.files()
                .list(
                    q=q,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    fields="files(id,name,appProperties)",
                )
                .execute(num_retries=3)
            )
            return resp.get("files")
        except HttpError as e:
            logging.error(f"Unable to list files with provided requirements: {e}")
            return None

    @staticmethod
    def update_file(
        file_id, payload, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """Update File"""
        if not client:
            client = DriveService(user_email).get()
        try:
            (
                client.files()
                .update(fileId=file_id, supportsAllDrives=True, body=payload)
                .execute(num_retries=3)
            )
            return True
        except HttpError as e:
            logging.error(
                f"Unable to update file {file_id} with payload {payload}: {e}"
            )
            return None

    @staticmethod
    def delete_file(
        file_id, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):

        """Delete File"""
        if not client:
            client = DriveService(user_email).get()
        try:
            (
                client.files()
                .delete(fileId=file_id, supportsAllDrives=True)
                .execute(num_retries=3)
            )
            return True
        except HttpError as e:
            logging.error(f"Unable to delete file {file_id} : {e}")
            return None

    @staticmethod
    def _download_file(request):
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh

    @staticmethod
    def export_file(file_id, user_email, mime_type="application/pdf", client=None):
        """Export a file to the given mime_type"""
        if not client:
            client = DriveService(user_email).get()

        try:
            request = client.files().export_media(fileId=file_id, mimeType=mime_type)
            return DriveUtils._download_file(request)
        except HttpError as e:
            logging.error(f"Unable to export file {file_id} : {e}")
            return None

    @staticmethod
    def download_file(file_id, user_email, client=None):
        """Download a file"""
        if not client:
            client = DriveService(user_email).get()

        db_file = DriveUtils.get_file(
            file_id,
            fields="name,mimeType,fullFileExtension",
            user_email=user_email,
            client=client,
        )
        if not db_file:
            return None, None, None

        if db_file.get("mimeType") in GOOGLE_DRIVE_MIMETYPES:
            return (
                DriveUtils.export_file(file_id, user_email, client=client),
                f"{db_file.get('name')}.pdf",
                "application/pdf",
            )
        else:
            ext = db_file.get("fullFileExtension")
            file_name = (
                db_file.get("name")
                if db_file.get("name").endswith(ext)
                else f"{db_file.get('name')}.{db_file.get('fullFileExtension')}"
            )
            try:
                request = client.files().get_media(fileId=file_id)
                return (
                    DriveUtils._download_file(request),
                    file_name,
                    db_file.get("mimeType"),
                )
            except HttpError as e:
                logging.error(f"Unable to download file {file_id} : {e}")

        return None, None, None

    @staticmethod
    def upload_file(
        user_email,
        file,
        filename,
        mimetype,
        parent_folder_id,
        properties=None,
        client=None,
    ):
        """Upload a file from the provided server path"""
        if not client:
            client = DriveService(user_email).get()
        file_metadata = {"name": filename, "parents": [parent_folder_id]}
        if properties is not None:
            file_metadata["appProperties"] = properties
        media = MediaIoBaseUpload(file, mimetype=mimetype, resumable=True)
        try:
            return (
                client.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    supportsAllDrives=True,
                    fields="id",
                )
                .execute()
            )

        except HttpError as e:
            logging.error(f"Unable to upload file {filename} : {e}")
            return None
