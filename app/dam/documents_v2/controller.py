from app.dam.documents.exceptions import InvalidSourceException
from app.dam.documents_v2.service import (
    DocumentGenerationV2Service,
    DocumentV2Sources,
)
from . import api
from flask import request
from flask_accepts import accepts, responds
from ...common.api import AuthenticatedApi
from .schema import DocumentGenerateSchema


@api.route("/")
class DocumentResource(AuthenticatedApi):
    """Documents"""

    @accepts(schema=DocumentGenerateSchema, api=api)
    def post(self):
        """Generate a document completed from template"""
        data = request.get_json(force=True)

        if data.get("source") not in DocumentV2Sources.__members__:
            raise InvalidSourceException

        DocumentGenerationV2Service.generate_document(
            template_id=data.get("template_id"),
            source=data.get("source"),
            user_email=data.get("user_email"),
            mission_id=data.get("mission_id"),
            copro_folder_id=data.get("copro_folder_id", None),
            thematic_folder_id=data.get("thematique_folder_id", None),
        )

        return "OK"
