from firebase_admin import firestore
from flask import current_app


class FirestoreUtils:
    def __init__(self):
        self.client = firestore.client()

    def list_items(self, collection):
        return self.client.collection(collection).get()

    def query_templates(self, scope=None, thematique_name=None):
        query = self.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_TEMPLATE_COLLECTION")
        )
        if scope:
            query = query.where("scope", "==", scope)
        if thematique_name:
            query = query.where("thematique_name", "==", thematique_name)
        return query.get()

    def query_version(
        self,
        thematique_name=None,
        resource_id=None,
        scope=None,
        version_name=None,
        version_date=None,
    ):
        query = self.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
        )
        if thematique_name:
            query = query.where("thematique_name", "==", thematique_name)
        if resource_id:
            query = query.where("resource_id", "==", resource_id)
        if scope:
            query = query.where("scope", "==", scope)
        if version_name:
            query = query.where("version_name", "==", version_name)
        if version_date:
            query = query.where("version_date", "==", version_date)

        return query.get()

    def get_version_by_id(self, version_id):
        return (
            self.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .document(version_id)
            .get()
        )

    def get_step_by_id(self, version_id, step_id):
        return (
            self.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .document(version_id)
            .collection(current_app.config.get("FIRESTORE_STEPS_COLLECTION"))
            .document(step_id)
            .get()
        )

    def create_version(self, version):
        document = self.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
        ).document()
        document.set(version)
        return document.id
