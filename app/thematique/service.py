from flask import current_app, jsonify

from app.common.firestore_utils import FirestoreUtils
from app.thematique.exceptions import (
    VersionNotFoundException,
    InvalidScopeException,
    InvalidResourceIdException,
    MissingVersionIdException,
    MissingStepIdException,
)
from app.thematique.schema import StepSchema


class ThematiqueService:
    @staticmethod
    def list_templates(scope=None, name=None):
        thematiques = []
        thematiques_added = []
        firestore_service = FirestoreUtils()
        all_templates_query = firestore_service.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_TEMPLATE_COLLECTION")
        )
        if scope and scope != "mission":
            all_templates_query = all_templates_query.where("scope", "==", scope)

        if name:
            all_templates_query = all_templates_query.where(
                "thematique_name", "==", name
            )

        for doc in all_templates_query.get():
            to_dict = doc.to_dict()
            to_dict["id"] = doc.id

            if scope == "mission":
                if to_dict.get("thematique_name") not in thematiques_added:
                    thematiques_added.append(to_dict.get("thematique_name"))
                    # del to_dict["scope"]
                    # del to_dict["legendes"]
                else:
                    continue
            else:
                to_dict["steps"] = ThematiqueService.handle_steps(doc)
            thematiques.append(to_dict)

        return thematiques

    @staticmethod
    def list_thematiques(scope, resource_id, thematique_name):
        firestore_service = FirestoreUtils()
        versions = []
        documents = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .where("scope", "==", scope)
            .where("resource_id", "==", resource_id)
            .where("thematique_name", "==", thematique_name)
            .get()
        )
        for d in documents:
            dict_obj = d.to_dict()
            dict_obj["id"] = d.id
            dict_obj["steps"] = ThematiqueService.handle_steps(d, copy_ids=True)
            versions.append(dict_obj)
        return versions

    @staticmethod
    def handle_steps(doc, copy_ids=False):
        steps = doc.reference.collection(
            current_app.config.get("FIRESTORE_STEPS_COLLECTION")
        ).get()
        step_list = []
        for s in steps:
            s_obj = s.to_dict()
            if copy_ids:
                s_obj["metadata"]["id"] = s.id
            step_list.append(s_obj)
        return step_list

    @staticmethod
    def get_version(version_id):
        firestore_service = FirestoreUtils()
        version = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .document(version_id)
            .get()
        )
        if version:
            version_dict = version.to_dict()
            version_dict["steps"] = ThematiqueService.handle_steps(
                version, copy_ids=True
            )
            return version_dict
        raise VersionNotFoundException

    @staticmethod
    def list_versions(scope, resource_id, thematique_name):

        if scope in ["", None]:
            raise InvalidScopeException
        if resource_id in ["", None]:
            raise InvalidResourceIdException

        firestore_service = FirestoreUtils()
        doc_query = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .where("scope", "==", scope)
            .where("resource_id", "==", int(resource_id))
        )

        if thematique_name:
            doc_query = doc_query.where("thematique_name", "==", thematique_name)

        list_docs = []
        for doc in doc_query.get():
            doc_dict = doc.to_dict()
            doc_dict["id"] = doc.id
            doc_dict["steps"] = ThematiqueService.handle_steps(doc, copy_ids=True)
            list_docs.append(doc_dict)

        return list_docs

    @staticmethod
    def duplicate_thematique(version):
        firestore_service = FirestoreUtils()
        steps = version.get("steps", [])
        del version["steps"]
        document = firestore_service.client.collection(
            current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
        ).document()
        document.set(version)
        for s in steps:
            step_doc = document.collection(
                current_app.config.get("FIRESTORE_STEPS_COLLECTION")
            ).document()
            step_doc.set(s)
        return ThematiqueService.get_version(document.id)

    @staticmethod
    def update_step(version_id: str, step_id: str, payload: StepSchema):

        if version_id in ["", None]:
            raise MissingVersionIdException
        if step_id in ["", None]:
            raise MissingStepIdException

        firestore_service = FirestoreUtils()
        step = (
            firestore_service.client.collection(
                current_app.config.get("FIRESTORE_THEMATIQUE_COLLECTION")
            )
            .document(version_id)
            .collection(current_app.config.get("FIRESTORE_STEPS_COLLECTION"))
            .document(step_id)
        )

        for key in ["legendes", "name", "order", "id"]:
            if key in payload["metadata"]:
                del payload["metadata"][key]

        step.set(payload, merge=True)
        return ThematiqueService.get_version(version_id)


    @staticmethod
    def get_thematiques_from_mission(mission_id):
        return [
            {
                "mision_id": mission_id,
                "thematique_name": "SUIVI_FINANCEMENT",
                "authorized": True
            }
        ]
