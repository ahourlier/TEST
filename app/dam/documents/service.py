import json
import os
from enum import Enum

from flask import request, g, jsonify
from sqlalchemy import or_

from flask_sqlalchemy import Pagination

from app import db
from app.common.config_error_messages import (
    KEY_SHARED_DRIVE_COPY_EXCEPTION,
    KEY_SHARED_DRIVE_FETCH_EXCEPTION,
    KEY_GOOGLE_DOCS_GET_EXCEPTION,
    KEY_GOOGLE_DOCS_UPDATE_EXCEPTION,
    KEY_GOOGLE_SHEETS_GET_EXCEPTION,
    KEY_GOOGLE_SHEETS_UPDATE_EXCEPTION,
)
from app.common.docs_utils import DocsUtils
from app.common.drive_utils import DriveUtils, DRIVE_DEFAULT_FIELDS
from app.common.exceptions import (
    InconsistentUpdateIdException,
    GoogleDocsException,
    GoogleSheetsException,
)
from app.common.search import sort_query
from app.common.sheets_util import SheetsUtils
from app.common.tasks import create_task
from app.common.templating_utils import TemplatingUtils
from app.dam.documents import Document, api
from app.dam.documents.error_handlers import (
    DocumentNotFoundException,
    InvalidSourceException,
    SharedDriveException,
    shared_drive_exception
)
from app.dam.documents.interface import DocumentInterface

import app.project.projects.service as projects_service

DOCUMENTS_DEFAULT_PAGE = 1
DOCUMENTS_DEFAULT_PAGE_SIZE = 100
DOCUMENTS_DEFAULT_SORT_FIELD = "id"
DOCUMENTS_DEFAULT_SORT_DIRECTION = "desc"

DOC_GENERATION_QUEUE_NAME = "document-generation-queue"
DOC_EDIT_QUEUE_NAME = "document-edit-queue"


class DocumentStatus(Enum):
    ON_GOING = "En cours"
    CREATED = "Créé"
    ERROR = "Erreur"


class DocumentSources(Enum):
    ATTACHMENT = "ATTACHMENT"
    REQUESTER = "REQUESTER"
    ACCOMMODATION = "ACCOMMODATION"


class DocumentGenerationService:
    @staticmethod
    def generate_document(document: Document, user_email=None):

        project = projects_service.ProjectService.get_by_id(document.project_id)
        template = DriveUtils.get_file(document.template_id, user_email=user_email)
        if template is not None:
            name = f'{template.get("name")} - Projet/{project.code_name}'
        else:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            resp, code = shared_drive_exception(SharedDriveException())
            resp.code = code
            return jsonify(resp)

        dest_folder = None

        if document.source == DocumentSources.ATTACHMENT.value:
            dest_folder = project.sd_root_folder_id
        elif document.source == DocumentSources.REQUESTER.value:
            dest_folder = project.sd_requester_folder_id
        elif document.source == DocumentSources.ACCOMMODATION.value:
            dest_folder = project.sd_accommodation_report_folder_id

        properties = {
            "projectId": project.id,
            "missionId": project.mission_id,
            "kind": document.source,
        }
        if dest_folder is not None:
            resp = DriveUtils.copy_file(
                document.template_id,
                dest_folder,
                name=name,
                properties=properties,
                user_email=user_email,
                fields=DRIVE_DEFAULT_FIELDS,
            )
            if not resp:
                DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
                raise SharedDriveException(KEY_SHARED_DRIVE_COPY_EXCEPTION)

            DocumentService.update(
                document, {"name": name, "document_id": resp.get("id")}
            )
            create_task(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("QUEUES_LOCATION"),
                queue=DOC_EDIT_QUEUE_NAME,
                uri=f"{os.getenv('API_URL')}/_internal/documents/edit",
                method="POST",
                payload={"document_id": document.id, "user_email": user_email},
            )

    @staticmethod
    def replace_document_placeholders(document: Document, user_email=None):

        file = DriveUtils.get_file(file_id=document.document_id, user_email=user_email)
        if file["mimeType"] == "application/vnd.google-apps.spreadsheet":
            DocumentGenerationService.replace_spreadsheet_placeholders(
                document, user_email
            )
        elif file["mimeType"] == "application/vnd.google-apps.document":
            DocumentGenerationService.replace_doc_placeholders(document, user_email)
        else:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            raise GoogleDocsException(KEY_GOOGLE_DOCS_UPDATE_EXCEPTION)

    @staticmethod
    def replace_doc_placeholders(document: Document, user_email=None):
        g_docs = DocsUtils.get_document(
            doc_id=document.document_id,
            user_email=user_email,
        )

        if not g_docs:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            raise GoogleDocsException(KEY_GOOGLE_DOCS_GET_EXCEPTION)

        placeholders = TemplatingUtils.extract_placeholders(g_docs)
        changes_mapper = TemplatingUtils.get_changes_mapper(
            placeholders, document.project_id
        )
        try:
            DocsUtils.update_document(
                doc_id=document.document_id,
                user_email=user_email,
                changes_map=changes_mapper,
            )
        except:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            raise GoogleDocsException(KEY_GOOGLE_DOCS_UPDATE_EXCEPTION)

        DocumentService.update(document, {"status": DocumentStatus.CREATED.value})

    @staticmethod
    def replace_spreadsheet_placeholders(document: Document, user_email=None):
        g_sheets = SheetsUtils.get_spreadsheet(
            spreasheet_id=document.document_id, user_email=user_email
        )

        if not g_sheets:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            raise GoogleSheetsException(KEY_GOOGLE_SHEETS_GET_EXCEPTION)

        placeholders = TemplatingUtils.extract_placeholders(g_sheets)
        changes_mapper = TemplatingUtils.get_changes_mapper(
            placeholders, document.project_id
        )
        try:
            SheetsUtils.batch_update_spreadsheet(
                spreadsheet_id=document.document_id,
                user_email=user_email,
                changes_map=changes_mapper,
            )
        except:
            DocumentService.update(document, {"status": DocumentStatus.ERROR.value})
            raise GoogleSheetsException(KEY_GOOGLE_SHEETS_UPDATE_EXCEPTION)

        DocumentService.update(document, {"status": DocumentStatus.CREATED.value})


class DocumentService:
    @staticmethod
    def get_all(
        page=DOCUMENTS_DEFAULT_PAGE,
        size=DOCUMENTS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=DOCUMENTS_DEFAULT_SORT_FIELD,
        direction=DOCUMENTS_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        q = sort_query(Document.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Document.name.ilike(search_term),
                    Document.tag.ilike(search_term),
                    Document.path.ilike(search_term),
                )
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(document_id: str) -> Document:
        db_document = Document.query.get(document_id)
        if db_document is None:
            raise DocumentNotFoundException
        return db_document

    @staticmethod
    def create(new_attrs: DocumentInterface) -> Document:
        """Generate a document from a given template"""

        projects_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        if new_attrs.get("source") not in DocumentSources.__members__:
            raise InvalidSourceException
        new_attrs["status"] = DocumentStatus.ON_GOING.value
        new_attrs["user_id"] = g.user.id
        document = Document(**new_attrs)
        db.session.add(document)
        db.session.commit()

        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=DOC_GENERATION_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/documents/generate",
            method="POST",
            payload={"document_id": document.id, "user_email": g.user.email},
        )
        return document

    @staticmethod
    def update(
        document: Document, changes: DocumentInterface, force_update: bool = False
    ) -> Document:
        if force_update or DocumentService.has_changed(document, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != document.id:
                raise InconsistentUpdateIdException
            document.update(changes)
            db.session.commit()
        return document

    @staticmethod
    def has_changed(document: Document, changes: DocumentInterface) -> bool:
        for key, value in changes.items():
            if getattr(document, key) != value:
                return True
        return False

    @staticmethod
    def html_document(new_attrs: DocumentInterface):
        """Return an HTML text based on a template, completed with corresponding values"""
        project = projects_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        html_doc = (
            DriveUtils.export_file(
                new_attrs.get("template_id"), g.user.email, mime_type="text/html"
            )
            .getvalue()
            .decode("utf-8")
        )
        placeholders = TemplatingUtils.extract_placeholders(html_doc)
        changes_mapper = TemplatingUtils.get_changes_mapper(placeholders, project.id)
        for key, value in changes_mapper.items():
            html_doc = html_doc.replace(key, value)
        # TODO some treatment here to avoid weird escapes and ASCII conversions ?
        return jsonify(dict(content=html_doc))

    # TODO To keep until we are sure it's not useful
    # @staticmethod
    # def delete_by_id(document_id: int) -> int or None:
    #     document = Document.query.filter(Document.id == document_id).first()
    #     if not document:
    #         raise DocumentNotFoundException
    #     db.session.delete(document)
    #     db.session.commit()
    #     return document_id
