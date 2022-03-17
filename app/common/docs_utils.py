import logging
import os

from app.common.google_apis import DocsService
from googleapiclient.errors import HttpError


class DocsUtils:
    @staticmethod
    def get_document(
        doc_id, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None,
    ):
        """Get a document"""
        if not client:
            client = DocsService(user_email).get()
        try:
            resp = client.documents().get(documentId=doc_id).execute(num_retries=3)
            return resp
        except HttpError as e:
            logging.error(f"Unable to get file {doc_id}: {e}")
            return None

    @staticmethod
    def update_document(
        doc_id,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        changes_map={},
    ):
        """Update a document"""
        if not client:
            client = DocsService(user_email).get()

        requests = []
        for key in changes_map:
            replacement_request = {
                "replaceAllText": {
                    "replaceText": changes_map[key],
                    "containsText": {"text": key, "matchCase": True},
                }
            }
            requests.append(replacement_request)

        payload = {"requests": requests}
        try:
            resp = (
                client.documents()
                .batchUpdate(documentId=doc_id, body=payload)
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to update file {doc_id}: {e}")
            return None
