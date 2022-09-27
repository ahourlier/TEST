from flask import request, logging, g

from app.internal_api.base import InternalAPIView
from app.dam.documents.service import DocumentService, DocumentGenerationService


class DocsGenerationV2View(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_document = DocumentService.get_by_id(data.get("document_id"))
        DocumentGenerationService.generate_document(
            db_document, user_email=data.get("user_email")
        )

        return "OK"


class DocsEditV2View(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        db_document = DocumentService.get_by_id(data.get("document_id"))
        DocumentGenerationService.replace_document_placeholders(
            db_document, user_email=data.get("user_email")
        )

        return "OK"
