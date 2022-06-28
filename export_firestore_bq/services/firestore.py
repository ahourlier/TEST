import os
from google.cloud import firestore

VERSIONS_COLLECTION = "thematiques"
STEPS_COLLECTION = "steps"
TEMPLATES_COLLECTION = "thematiques_template"


class FirestoreUtils:
    def __init__(self):
        self.client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))

    def list_items(self, collection):
        return self.client.collection(collection).get()

    def list_templates(self):
        return self.list_items(TEMPLATES_COLLECTION)

    def query_version(
        self,
        thematique_name=None,
        resource_id=None,
        scope=None,
        version_name=None,
        version_date=None,
    ):
        query = self.client.collection(VERSIONS_COLLECTION)
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
        return self.client.collection(VERSIONS_COLLECTION).document(version_id).get()

    def get_steps_by_version_id(self, version_id):
        return (
            self.client.collection(VERSIONS_COLLECTION)
            .document(version_id)
            .collection(STEPS_COLLECTION)
            .get()
        )

    def get_step_by_id(self, version_id, step_id):
        return (
            self.client.collection(VERSIONS_COLLECTION)
            .document(version_id)
            .collection(STEPS_COLLECTION)
            .document(step_id)
            .get()
        )
